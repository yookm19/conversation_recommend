# -*- coding: utf-8 -*-

from flask import Flask, render_template, request, redirect, url_for
from bottle import route, run
from module.language_understanding import NaturalLanguageUnderstanding

app = Flask(__name__)

@app.route('/test',methods=['POST'])
def test_post():
    msg = request.params.decode().get('message')
    analyze = NaturalLanguageUnderstanding()
    result = analyze.analyze_sentence(msg)
    return result

# 音声認識
@app.route('/')
def index():
    return '''
      <!DOCTYPE html>
      <html lang="ja">
      <head>
          <meta charset="UTF-8">
          <title>会話補助アプリ</title>
      </head>
      <body>
          <h2>会話補助アプリ</h2>
          <button id="start">start</button>
          <div id="content"></div>
          <div>
              <textarea id="text" rows="5"></textarea>
              <button id="manual" onclick="manual()">手動送信</button>
              <button id="send" onclick="send()">send</button>
          </div>
          <a>Tweets</a>
          <div id="tweets"></div>
              
        <script>        
            function time(){
              var date = new Date();
              var hh = ("0"+date.getHours()).slice(-2);
              var min = ("0"+date.getMinutes()).slice(-2);
              var sec = ("0"+date.getSeconds()).slice(-2);
          
              var time = hh+":"+min+":"+sec;
              return time;
            }
        
          //ここに音声認識の処理を書いていく
          const speech = new webkitSpeechRecognition();
          speech.lang = 'ja-JP';

          //使用する変数を用意
          const btn = document.getElementById('start');
          const content = document.getElementById('content');

          btn.addEventListener('click', function(){
              //音声認識をスタート
              speech.start();
          });

          // 音声自動文字起こし機能
          speech.onresult = function(e){
              speech.stop();
              if(e.results[0].isFinal){
                  var autotext = e.results[0][0].transcript
                  console.log(e);
                  console.log(autotext);
                  content.innerHTML += '<div>'+ autotext + '</div>';
              }
          }

          speech.onend = () => {
              speech.start()
          };

          // テキストボックス内の値を手動送信
          var manual = function(){
              var text = document.getElementById('text').value;
              content.innerHTML += '<div>'+text+'</div>';
          };


          // 文字起こし結果を送信
          var send = function(){
              //var tweets = document.getElementById('tweets');
              //console.log(content.innerText);
              var msg = content.innerText;
              
              //tweets.innerHTML += '<div>'+msg+'</div>';

             $ py({
               type:"POST",
               url:"/test",
               data:"message="+msg,
               success:tweet_func
             });
          };

          // カンペTweetを表示
          var tweet_func = function(reply){
              var tweets = document.getElementById('tweets');
              tweets.innerHTML += '<div>'+reply+'</div>';
          }

        </script>
        </body>
      </html>
    '''


if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=3000)
