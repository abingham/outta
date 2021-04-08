module Main exposing (Msg(..), main, update, view)

import Bootstrap.Button as Button
import Bootstrap.CDN as CDN
import Bootstrap.Form as Form
import Bootstrap.Form.Input as Input
import Bootstrap.Form.InputGroup as InputGroup
import Bootstrap.Grid as Grid
import Bootstrap.Table as Table
import Browser
import Html exposing (Html, button, div, input, table, td, text, tr)
import Html.Events exposing (onClick, onInput)
import Http
import Json.Decode as Decode exposing (Decoder, float, int, list, string)
import Json.Decode.Pipeline exposing (hardcoded, optional, required)
import Json.Encode as Encode
import List
import Url.Builder



-- TODO: Don't hardcode the API URL


type alias Element =
    { description : String
    , text : String
    }


translationRequest : String -> Encode.Value
translationRequest text =
    Encode.object
        [ ( "text", Encode.string text ) ]


type alias Model =
    { text : String
    , response : List Element
    }


elementDecoder : Decoder Element
elementDecoder =
    Decode.succeed Element
        |> required "description" string
        |> required "text" string


init : () -> ( Model, Cmd Msg )
init _ =
    ( { text = ""
      , response = []
      }
    , Cmd.none
    )


type Msg
    = InputTextChanged String
    | TranslationRequested
    | TranslationResponseReceived (Result Http.Error (List Element))


errorToString : Http.Error -> String
errorToString error =
    case error of
        Http.BadUrl url ->
            "The URL " ++ url ++ " was invalid"

        Http.Timeout ->
            "Unable to reach the server, try again"

        Http.NetworkError ->
            "Unable to reach the server, check your network connection"

        Http.BadStatus 500 ->
            "The server had a problem, try again later"

        Http.BadStatus 400 ->
            "Verify your information and try again"

        Http.BadStatus _ ->
            "Unknown error"

        Http.BadBody errorMessage ->
            errorMessage


update : Msg -> Model -> ( Model, Cmd Msg )
update msg model =
    case msg of
        InputTextChanged text ->
            ( { model | text = text }, Cmd.none )

        TranslationRequested ->
            let
                text =
                    String.replace "\\x1b" "\u{001B}" model.text

                url =
                    Url.Builder.crossOrigin "http://localhost:8000" [] [ Url.Builder.string "text" text ]
            in
            ( { model | text = "" }
            , Http.get
                { url = url
                , expect = Http.expectJson TranslationResponseReceived (list elementDecoder)
                }
            )

        TranslationResponseReceived (Ok elements) ->
            ( { model | response = elements }, Cmd.none )

        -- TODO: Log the error
        TranslationResponseReceived (Err err) ->
            ( { model | response = [ Element "error" (errorToString err) ] }, Cmd.none )


mainContent : Model -> Html.Html Msg
mainContent model =
    let
        rows =
            List.map
                (\e ->
                    Table.tr [ Table.rowInfo ]
                        [ Table.td [] [ text e.text ]
                        , Table.td [] [ text e.description ]
                        ]
                )
                model.response

        responseTable =
            Table.simpleTable
                ( Table.simpleThead
                    [ Table.th [] [ text "Text" ]
                    , Table.th [] [ text "Description" ]
                    ]
                , Table.tbody [] rows
                )
    in
    div []
        [ InputGroup.config
            (InputGroup.text [ Input.onInput InputTextChanged, Input.value model.text ])
            |> InputGroup.large
            |> InputGroup.successors
                [ InputGroup.button [ Button.primary, Button.onClick TranslationRequested ] [ text "Translate" ] ]
            |> InputGroup.view
        , responseTable
        ]


view : Model -> Html Msg
view model =
    Grid.container []
        -- Responsive fixed width container
        [ CDN.stylesheet -- Inlined Bootstrap CSS for use with reactor

        -- , navbar model -- Interactive and responsive menu
        , mainContent model
        ]


subscriptions : Model -> Sub Msg
subscriptions model =
    Sub.none


main =
    Browser.element
        { init = init
        , update = update
        , subscriptions = subscriptions
        , view = view
        }
