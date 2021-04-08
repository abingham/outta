module Outta.View exposing (view)

import Bootstrap.Button as Button
import Bootstrap.CDN as CDN
import Bootstrap.Form.Input as Input
import Bootstrap.Form.InputGroup as InputGroup
import Bootstrap.Grid as Grid
import Bootstrap.Table as Table
import Html exposing (Html, div, text)
import List
import Outta.Model exposing (Model)
import Outta.Msg exposing (..)


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
            (InputGroup.text
                [ Input.onInput InputTextChanged
                , Input.value model.text
                , Input.placeholder "Enter text containing control codes for translation..."
                ]
            )
            |> InputGroup.large
            |> InputGroup.successors
                [ InputGroup.button
                    [ Button.primary
                    , Button.onClick TranslationRequested
                    ]
                    [ text "Translate" ]
                ]
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
