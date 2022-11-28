# GUI4CV2_Tkinter  
GUI for OpenCV-Python with Tkinter  
・OpenCV-Pyhtonの簡易設定画面を持ったツールです。  
・画面はpygubu-designer(Tkinter)で作成されています。  
・画像処理は素人なので間違いがあるかもしれません。  
  
必要なライブラリ  
・OpenCV-Python  
・numpy  
・tkinter
  
単体動作（ぼかし）  
![スクリーンショット_2022-09-24_11-13-54](https://user-images.githubusercontent.com/86605611/192075844-00cecf9b-a432-4740-b0da-f4ccbdbb8d80.png)

  
アプリ動作（画像処理をリストから追加してパラメータを設定していく）  
![スクリーンショット_2022-09-24_11-20-44](https://user-images.githubusercontent.com/86605611/192076052-25b7f997-86cd-4de7-a650-48c55700d2cc.png)
![スクリーンショット_2022-09-24_11-21-52](https://user-images.githubusercontent.com/86605611/192076061-6e088691-ed36-4180-971a-e33c218a0d89.png)

  
動画    
・単体：https://youtu.be/W58tFDa8cvc  
・アプリ：https://youtu.be/QmiHQ8GiGpE / https://youtu.be/M6mwR_ipujc  
  
実装済み  
・ファイル開く(Open File)  
・ファイル保存(Save File)  
・画像メモリ作成(Create IMG Memory)  
・画像メモリI/O(MemoryIO)  
・画像結合(ImageCombine)  
・濃淡補正 (MovingAve)  
・濃淡補正 (MovingAveColor)  
・濃淡補正 (ShadingApproximate)  
・濃淡補正 (ShadingBlur)  
・濃淡補正 (ShadingMediaBlur)  
・濃淡補正 (ShadingMediaBlurColor)  
・濃淡補正 (ShadingCustomFillter)  
・明るさ／コントラスト (ConvertScaleAbs)  
・ガンマ補正（Gamma）  
・ホワイトバランス (WhiteBalance)  
・平坦化 (EqualizeHist)  
・色反転 (Bitwise Not)  
・明度反転 (Reverse Brightness)  
・回転 (Rotate)  
・射影変換 (warpPerspective)  
・切り抜き (Trim)  
・ぼかし (Average)  
・ぼかし (Blur)  
・ぼかし (Median Blur)  
・ぼかし (Gaussian_Blur)  
・ぼかし (Bilateral_Filter)  
・ぼかし (FastNlMeansDenoisingColored)  
・シャープ (Filter2D)  
・シャープ (UnSharp)  
・膨張 (Dilate)  
・収縮 (Erode)  
・モルフォロジー (Morphology)  
・二値化 (Threshold)  
・二値化 (inRange)  
・二値化 (Adaptive_Thresholed)  
・輪郭抽出 (Canny)  
・輪郭抽出 (Laplacian)  
・輪郭抽出 (Sobel)  
・  
  
実装予定  
・その他画像処理  
・~~アプリで処理した内容のPythonコードを出力~~ 実装済み  
  
ブログ  
https://danpapa-hry.hateblo.jp/entry/2022/09/25/072516  
