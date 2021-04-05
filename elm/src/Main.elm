module Main exposing (Msg(..), main, update, view)

import Browser
import Html exposing (Html, button, div, input, text)
import Html.Events exposing (onClick, onInput)
import Http
import Json.Decode as Decode exposing (Decoder, float, int, list, string)
import Json.Decode.Pipeline exposing (hardcoded, optional, required)
import List



-- TODO: Don't hardcode the API URL


type alias Element =
    { description : String
    , text : String
    }


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


update : Msg -> Model -> ( Model, Cmd Msg )
update msg model =
    case msg of
        InputTextChanged text ->
            ( { model | text = text }, Cmd.none )

        TranslationRequested ->
            ( { model | text = "" }
            , Http.get
                -- TODO: encode the request in JSON
                { url = "localhost:8000/"
                , expect = Http.expectJson TranslationResponseReceived (list elementDecoder)
                }
            )

        TranslationResponseReceived (Ok elements) ->
            ( { model | response = elements }, Cmd.none )

        -- TODO: Log the error
        TranslationResponseReceived (Err _) ->
            ( { model | response = [] }, Cmd.none )


view : Model -> Html.Html Msg
view model =
    let
        elements =
            List.map (\e -> text e.text) model.response
    in
    div []
        [ input [ onInput InputTextChanged ] []
        , div [] [ text model.text ]
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
