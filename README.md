# FpsScoreAPP
URL:https://fpslist.herokuapp.com/polls  
テストユーザーとしてログインする際は、ゲストログインボタンを押してください。
## アプリケーション概要
FPSゲームの戦績を管理するアプリケーションである。  
ユーザーはゲームを一戦プレイするごとにその戦績(キル数、デス数、スコア数)を入力する。  
入力したデータはデータベースに保存されメイン画面で表として表示される。表のデータは削除可能である。    
より戦績を見やすくするために、1週間以内のキル数、デス数、スコア数、kdの値をグラフ化し表示する。  
## アプリケーション機能一覧
- ログイン機能  
- データ入力機能  
- データ削除機能  
- モーダルウィンドウ機能  
- 表作成機能
- グラフ作成機能  
## アプリケーションの詳細説明
- 言語はPython、javascript、css、htmlを使用  
- フレームワークは、djangoを使用  
- デザインは、bootstrapを使用  
- グラフの作成には、matplotlibを使用  
- 現在の日付の取得には、timezone、datetimeを使用  
- データを削除する際に、モーダルウィンドウを使用  
- models.py内のRecordクラスでデータベースのpolls_recordというテーブルを作成  
- データベースには、sqlite3を使用 
- デプロイには、herokuを使用   　　


