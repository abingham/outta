module Outta.Model exposing (Element, Model)


type alias Element =
    { description : String
    , text : String
    }


type alias Model =
    { text : String
    , response : List Element
    }
