#!/bin/bash

# チャットワークに出力
# チャットワークAPIトークン
CW_TOKEN=""
# チャットワーク部屋ID
CW_ROOM="************"       
# テキスト
MEMBER="************* "
TEXT_AREA="**********"
TEXT_AREA+="""自由に遅れます。"""
        
# エンドポイント
curl -X POST -H "X-ChatWorkToken:${CW_TOKEN}" -d "body=${MEMBER}+${TEXT_AREA}" "https://api.chatwork.com/v2/rooms/${CW_ROOM}/messages"
