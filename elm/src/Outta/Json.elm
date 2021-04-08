module Outta.Json exposing (..)

import Json.Decode as Decode
import Json.Decode.Pipeline exposing (required)
import Json.Encode as Encode
import Outta.Model exposing (Element)


translationRequest : String -> Encode.Value
translationRequest text =
    Encode.object
        [ ( "text", Encode.string text ) ]


elementDecoder : Decode.Decoder Element
elementDecoder =
    Decode.succeed Element
        |> required "description" Decode.string
        |> required "text" Decode.string
