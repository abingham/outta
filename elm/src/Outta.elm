module Outta exposing (main)

import Browser
import Outta.Model exposing (Model)
import Outta.Msg exposing (..)
import Outta.Update exposing (update)
import Outta.View


init : () -> ( Model, Cmd Msg )
init _ =
    ( { text = ""
      , response = []
      }
    , Cmd.none
    )


subscriptions : Model -> Sub Msg
subscriptions _ =
    Sub.none


main : Program () Model Msg
main =
    Browser.element
        { init = init
        , update = update
        , subscriptions = subscriptions
        , view = Outta.View.view
        }
