module Outta.Msg exposing (..)

import Http
import Outta.Model exposing (Element)


type Msg
    = InputTextChanged String
    | TranslationRequested
    | TranslationResponseReceived (Result Http.Error (List Element))
