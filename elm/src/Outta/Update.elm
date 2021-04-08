module Outta.Update exposing (update)

import Http
import Json.Decode exposing (list)
import Outta.Json exposing (elementDecoder)
import Outta.Model exposing (Element, Model)
import Outta.Msg exposing (..)
import Url.Builder


update : Msg -> Model -> ( Model, Cmd Msg )
update msg model =
    case msg of
        InputTextChanged text ->
            ( { model | text = text }, Cmd.none )

        TranslationRequested ->
            let
                text =
                    String.replace "\\x1b" "\u{001B}" model.text

                -- TODO: Don't hardcode the API URL
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
