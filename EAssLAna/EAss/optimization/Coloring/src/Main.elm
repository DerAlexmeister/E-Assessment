module Main exposing (..)

import Browser
import Browser.Navigation exposing (load)
import Dict.Any as D
import EverySet as S
import Four exposing (Four, Index(..), Karnaugh, decodeIndex, enumFour, get2d, repeat, toInt)
import Html exposing (Html, button, div, p, table, td, text, th, tr)
import Html.Attributes exposing (class, style)
import Html.Events exposing (onClick)
import Http
import Json.Decode as J exposing (index)
import Json.Encode as E
import List as L


host =
    "http://127.0.0.1:8000/eassessments/coloring"


type State
    = Marking Color
    | Idle (Maybe Color)


type alias Selection =
    S.EverySet ( Index, Index )


type alias Model =
    { karnaugh : Karnaugh
    , colors : D.AnyDict String Color Selection
    , colorings : D.AnyDict ( Int, Int ) ( Index, Index ) (S.EverySet Color)
    , state : State
    , variables : Four String
    , token : String
    , response : Maybe String
    }


type Message
    = ClickKarnaugh Index Index
    | AddColor
    | RemoveColor
    | FinishColoring
    | SelectColor Color
    | Submit
    | Submitted String


type alias Flag =
    { input : J.Value
    , token : String
    }


main : Program Flag Model Message
main =
    Browser.element
        { init = init
        , view = view
        , update = update
        , subscriptions = subscriptions
        }


init : Flag -> ( Model, Cmd Message )
init flag =
    let
        input =
            J.decodeValue inputDecoder flag.input
                |> Result.withDefault
                    { problem = repeat (repeat False)
                    , coloring = D.empty colorName
                    }
    in
    ( { karnaugh = input.problem
      , colors = input.coloring
      , colorings = deriveColoring input.coloring
      , state = Idle Nothing
      , variables = Four "x1" "x2" "x3" "x4"
      , token = flag.token
      , response = Nothing
      }
    , Cmd.none
    )


removeColoring : Model -> Color -> Model
removeColoring model color =
    let
        new_colors =
            model.colors
                |> D.remove color

        new_colorings =
            model.colorings
                |> D.map (\_ -> S.remove color)
    in
    { model
        | colors = new_colors
        , colorings = new_colorings
        , state = Idle Nothing
    }


update : Message -> Model -> ( Model, Cmd Message )
update msg model =
    case ( msg, model.state ) of
        ( AddColor, _ ) ->
            let
                used_colors =
                    D.keys model.colors
                        |> S.fromList

                total_colors =
                    enumColors
                        |> S.fromList

                available_colors =
                    S.diff total_colors used_colors
                        |> S.toList
            in
            case L.head available_colors of
                Just color ->
                    ( { model
                        | state = Marking color
                        , colors = D.insert color S.empty model.colors
                      }
                    , Cmd.none
                    )

                Nothing ->
                    ( model, Cmd.none )

        ( RemoveColor, Marking color ) ->
            ( removeColoring model color, Cmd.none )

        ( RemoveColor, Idle (Just color) ) ->
            ( removeColoring model color, Cmd.none )

        ( SelectColor color, _ ) ->
            ( { model | state = Marking color }, Cmd.none )

        ( ClickKarnaugh x y, Marking color ) ->
            ( case D.get color model.colors of
                Just working_set ->
                    if S.member ( x, y ) working_set then
                        let
                            new_set =
                                S.remove ( x, y ) working_set

                            new_coloring =
                                D.get ( x, y ) model.colorings
                                    |> Maybe.withDefault S.empty
                                    |> S.remove color
                        in
                        { model
                            | colors = D.insert color new_set model.colors
                            , colorings = D.insert ( x, y ) new_coloring model.colorings
                        }

                    else
                        let
                            new_set =
                                S.insert ( x, y ) working_set

                            new_coloring =
                                D.get ( x, y ) model.colorings
                                    |> Maybe.withDefault S.empty
                                    |> S.insert color
                        in
                        { model
                            | colors = D.insert color new_set model.colors
                            , colorings = D.insert ( x, y ) new_coloring model.colorings
                        }

                Nothing ->
                    model
            , Cmd.none
            )

        ( FinishColoring, _ ) ->
            ( { model | state = Idle Nothing }, Cmd.none )

        ( Submit, _ ) ->
            ( model
            , Http.request
                { method = "POST"
                , headers = [ Http.header "X-CSRFToken" model.token ]
                , url = host
                , body = Http.jsonBody <| encodeSubmission <| Submission model.karnaugh model.colors
                , expect =
                    Http.expectString <|
                        \response ->
                            case response of
                                Ok str ->
                                    Submitted str

                                Err _ ->
                                    Submitted "An error occurred!"
                , timeout = Nothing
                , tracker = Nothing
                }
            )

        ( Submitted response, _ ) ->
            ( { model | response = Just response }, Cmd.none )

        _ ->
            ( model, Cmd.none )


fromBool : Bool -> String
fromBool b =
    if b then
        "1"

    else
        "0"


rowValues : Four String
rowValues =
    Four "00" "01" "11" "10"


columnValues : Four String
columnValues =
    Four "10" "11" "01" "00"


entryToString : Index -> Index -> String
entryToString x y =
    Four.get x rowValues ++ Four.get y columnValues


tableCaption : Four String -> Html msg
tableCaption four =
    th []
        [ text <|
            four.two
                ++ four.three
                ++ "\\"
                ++ four.zero
                ++ four.one
        ]


rowCaption : Four String -> Html msg
rowCaption variables =
    rowValues
        |> Four.map text
        |> Four.map (\t -> th [] [ t ])
        |> Four.toList
        |> (\l -> tableCaption variables :: l)
        |> tr []


columnCaption : Index -> Html msg
columnCaption index =
    columnValues
        |> Four.get index
        |> text


viewDatum : Model -> Index -> Index -> Html Message
viewDatum model x y =
    td []
        [ chooseColoring model x y
            |> (\t ->
                    applyColoring t
                        (button
                            [ onClick (ClickKarnaugh x y) ]
                            [ text (fromBool (get2d x y model.karnaugh)) ]
                        )
               )
        ]


viewRow : Model -> Index -> Html Message
viewRow model x =
    tr [] (columnCaption x :: L.map (viewDatum model x) enumFour)


viewKarnaugh : Four String -> Model -> Html Message
viewKarnaugh variables model =
    enumFour
        |> L.map (viewRow model)
        |> (\l -> rowCaption variables :: l)
        |> table []


viewSelection : Color -> Selection -> Html Message
viewSelection color selection =
    S.toList selection
        |> L.map (\( x, y ) -> entryToString x y)
        |> String.join ", "
        |> text
        |> L.singleton
        |> button
            [ onClick <| SelectColor color
            , style "border-color" <| colorName color
            ]


viewColoring : Maybe Color -> D.AnyDict String Color Selection -> Html Message
viewColoring color coloring =
    coloring
        |> D.toList
        |> L.map
            (\( c, selection ) ->
                ( c, viewSelection c selection )
            )
        |> L.map
            (\( c, selection ) ->
                p
                    (if Just c == color then
                        [ style "background-color" "red" ]

                     else
                        []
                    )
                    [ selection ]
            )
        |> div []


view : Model -> Html Message
view model =
    let
        index =
            case model.state of
                Marking i ->
                    Just i

                Idle i ->
                    i
    in
    div [] <|
        L.foldr tryAppend [] <|
            [ Just <| viewKarnaugh model.variables model
            , Just <| viewColoring index model.colors
            , addColorButton model
            , removeColorButton model
            , finishColoringButton model
            , Just <| button [ onClick Submit ] [ text "Submit" ]
            , Maybe.map text model.response
            ]


try : Bool -> a -> Maybe a
try pred a =
    if pred then
        Just a

    else
        Nothing


tryAppend : Maybe a -> List a -> List a
tryAppend ma l =
    case ma of
        Just a ->
            a :: l

        Nothing ->
            l


addColorButtonStyle : List (Html.Attribute Message)
addColorButtonStyle =
    [ onClick AddColor, class "add-color", class "coloring-button" ]


addColorButton : Model -> Maybe (Html Message)
addColorButton model =
    try (D.size model.colors < L.length enumColors) <|
        button
            addColorButtonStyle
            [ text "Add Cover" ]


removeColorButtonStyle : List (Html.Attribute Message)
removeColorButtonStyle =
    [ onClick RemoveColor
    , class "remove-color"
    , class "coloring-button"
    ]


removeColorButton : Model -> Maybe (Html Message)
removeColorButton model =
    case model.state of
        Marking _ ->
            try (D.size model.colors >= 1) <|
                button
                    removeColorButtonStyle
                    [ text "Remove Color" ]

        _ ->
            Nothing


finishColoringButtonStyle : List (Html.Attribute Message)
finishColoringButtonStyle =
    [ onClick FinishColoring
    , class "finish-coloring-color"
    , class "coloring-button"
    ]


finishColoringButton : Model -> Maybe (Html Message)
finishColoringButton model =
    case model.state of
        Marking _ ->
            Just <|
                button
                    finishColoringButtonStyle
                    [ text "Finish Selection" ]

        _ ->
            Nothing


chooseColoring : Model -> Index -> Index -> List (Maybe Color)
chooseColoring model x y =
    let
        colors =
            model.colorings
                |> D.get ( x, y )
                |> Maybe.withDefault S.empty
    in
    enumColors
        |> L.map
            (\color ->
                if S.member color colors then
                    Just color

                else
                    Nothing
            )


applyColoring : List (Maybe Color) -> Html msg -> Html msg
applyColoring colors inner =
    L.foldr coloringStyle inner colors


activeColoringFrameStyle : List (Html.Attribute msg)
activeColoringFrameStyle =
    [ style "border-style" "dashed"
    ]


deactiveColoringFrameStyle : List (Html.Attribute msg)
deactiveColoringFrameStyle =
    [ style "border-color" "white"
    , style "border-style" "solid"
    ]


coloringFrameStyle : List (Html.Attribute msg)
coloringFrameStyle =
    [ style "padding" "2px"
    , style "margin" "2px "
    ]


coloringStyle : Maybe Color -> Html msg -> Html msg
coloringStyle color inner =
    color
        |> Maybe.map colorName
        |> Maybe.map (style "border-color")
        |> Maybe.map L.singleton
        |> Maybe.map (L.append activeColoringFrameStyle)
        |> Maybe.withDefault deactiveColoringFrameStyle
        |> L.append coloringFrameStyle
        |> (\attr -> div attr [ inner ])


type Color
    = Red
    | Green
    | Blue
    | Purple


colorName : Color -> String
colorName c =
    case c of
        Red ->
            "red"

        Green ->
            "Green"

        Blue ->
            "blue"

        Purple ->
            "purple"


enumColors : List Color
enumColors =
    [ Red
    , Green
    , Blue
    , Purple
    ]


subscriptions : Model -> Sub Message
subscriptions _ =
    Sub.none


encodeSet : (a -> E.Value) -> S.EverySet a -> E.Value
encodeSet a set =
    set
        |> S.toList
        |> E.list a


decodeSet : J.Decoder a -> J.Decoder (S.EverySet a)
decodeSet a =
    J.map S.fromList <|
        J.list a


encodeIndexPair : ( Index, Index ) -> E.Value
encodeIndexPair ( x, y ) =
    [ x, y ]
        |> List.map toInt
        |> E.list E.int


decodeIndexPair : List Int -> J.Decoder ( Index, Index )
decodeIndexPair list =
    case list of
        [ i, j ] ->
            J.map2 Tuple.pair
                (decodeIndex i)
                (decodeIndex j)

        _ ->
            J.fail "Index pair should only have two elements"


encodeSelection : Selection -> E.Value
encodeSelection =
    encodeSet encodeIndexPair


decodeSelection : J.Decoder Selection
decodeSelection =
    decodeSet <|
        J.andThen decodeIndexPair <|
            J.list J.int


encodeColoring : D.AnyDict String Color Selection -> E.Value
encodeColoring =
    D.encode colorName encodeSelection


nameToColor : String -> Result String Color
nameToColor color =
    case color of
        "red" ->
            Ok Red

        "Green" ->
            Ok Green

        "blue" ->
            Ok Blue

        "purple" ->
            Ok Purple

        _ ->
            Err "Unknown color!"


coloringDecoder : J.Decoder (D.AnyDict String Color Selection)
coloringDecoder =
    D.decode_ (\str _ -> nameToColor str)
        colorName
        decodeSelection


deriveColoring : D.AnyDict String Color Selection -> D.AnyDict ( Int, Int ) ( Index, Index ) (S.EverySet Color)
deriveColoring colors =
    D.foldl
        (\color indices dict ->
            S.foldl
                (\index d ->
                    D.get index d
                        |> Maybe.withDefault S.empty
                        |> S.insert color
                        |> (\s -> D.insert index s d)
                )
                dict
                indices
        )
        (D.empty (\( x, y ) -> ( toInt x, toInt y )))
        colors


type alias Submission =
    { problem : Karnaugh
    , coloring : D.AnyDict String Color Selection
    }


encodeSubmission : Submission -> E.Value
encodeSubmission result =
    E.object
        [ ( "problem", Four.encodeKarnaugh result.problem )
        , ( "coloring", encodeColoring result.coloring )
        ]


inputDecoder : J.Decoder Submission
inputDecoder =
    J.map2 Submission
        (J.field "karnaugh" Four.karnaugh)
        (J.maybe (J.field "coloring" coloringDecoder)
            |> J.map (Maybe.withDefault <| D.empty colorName)
        )
