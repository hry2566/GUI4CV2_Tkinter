"""GUIアプリ"""
from functools import partial

from lib.app.cls_app_base import App_Base
from lib.cls_lib import *


class App(App_Base):
    """GUIアプリクラス"""

    def __init__(self, master=None):
        super().__init__(master)
        self.__init_proc_code()
        self.__init_gui()
        self.__init_events()

    def __init_gui(self):
        # ***********************************************************************
        labels_file = ['ファイル開く(Open File)',
                       'ファイル保存(Save File)']

        labels_image = ['回転 (Rotate)',
                        '位置合わせ (PhaseCorrelate_XY)',
                        '位置合わせ (PhaseCorrelate)',
                        'マスク処理 (Mask)',
                        '射影変換 (warpPerspective)',
                        '切り抜き (Trim)',
                        '画像結合 (ImageCombine)',
                        '最小外接円計測 (CircleDetection)',
                        'エッジ位置計測 (EdgeMeasurement)',
                        'エッジ位置_カスタム (Edge_Custom)',
                        'エッジ円周 (EdgeArc)']

        labels_color = ['明るさ／コントラスト (ConvertScaleAbs)',
                        'ガンマ補正 (Gamma)',
                        'ホワイトバランス (WhiteBalance)',
                        '平坦化 (EqualizeHist)',
                        '色反転 (Bitwise Not)',
                        '明度反転 (Reverse Brightness)',
                        '濃淡補正 (MovingAve)',
                        '濃淡補正 (MovingAveColor)',
                        '濃淡補正 (ShadingApproximate)',
                        '濃淡補正 (ShadingBlur)',
                        '濃淡補正 (ShadingMediaBlur)',
                        '濃淡補正 (ShadingMediaBlurColor)',
                        '濃淡補正 (ShadingCustomFillter)']

        menu_fillter = ['ぼかし (Average)',
                        'ぼかし (Blur)',
                        'ぼかし (MedianBlur)',
                        'ぼかし (GaussianBlur)',
                        'ぼかし (BilateralFilter)',
                        'ぼかし (FastNlMeansDenoisingColored)',
                        'シャープ (Filter2D)',
                        'シャープ (UnSharp)',
                        '膨張 (Dilate)',
                        '収縮 (Erode)',
                        'モルフォロジー (Morphology)',
                        '二値化 (Threshold)',
                        '二値化 (inRange)',
                        '二値化 (AdaptiveThresholed)',
                        '輪郭抽出 (Canny)',
                        '輪郭抽出 (Laplacian)',
                        '輪郭抽出 (Sobel)',
                        '輪郭抽出 (LaplacianCustom)']

        menu_memory = ['画像メモリ作成(Create IMG Memory)',
                       '画像メモリI/O(MemoryIO)']

        self.set_menu(self.menu_file, labels_file)
        self.set_menu(self.menu_image, labels_image)
        self.set_menu(self.menu_fillter, menu_fillter)
        self.set_menu(self.menu_color, labels_color)
        self.set_menu(self.menu_memory, menu_memory)

    def __init_events(self):
        pass

    def __init_proc_code(self):
        proc_code_list = []
        fnc_list = []
        proc_code_list.append(['ファイル開く(Open File)',
                               'OpenFile(param, gui=False)'])
        fnc_list.append(partial(OpenFile))

        proc_code_list.append(['ファイル保存(Save File)',
                               'SaveFile(img, param, gui=False)'])
        fnc_list.append(partial(SaveFile))

        proc_code_list.append(['ぼかし (Average)',
                               'Average(img, param, gui=False)'])
        fnc_list.append(partial(Average))

        proc_code_list.append(['二値化 (AdaptiveThresholed)',
                               'AdaptiveThresholed(img, param, gui=False)'])
        fnc_list.append(partial(AdaptiveThresholed))

        proc_code_list.append(['ぼかし (BilateralFilter)',
                               'BilateralFilter(img, param, gui=False)'])
        fnc_list.append(partial(BilateralFilter))

        proc_code_list.append(['ぼかし (Blur)',
                               'Blur(img, param, gui=False)'])
        fnc_list.append(partial(Blur))

        proc_code_list.append(['輪郭抽出 (Canny)',
                               'Canny(img, param, gui=False)'])
        fnc_list.append(partial(Canny))

        proc_code_list.append(['膨張 (Dilate)',
                               'Dilate(img, param, gui=False)'])
        fnc_list.append(partial(Dilate))

        proc_code_list.append(['収縮 (Erode)',
                               'Erode(img, param, gui=False)'])
        fnc_list.append(partial(Erode))

        proc_code_list.append(['シャープ (Filter2D)',
                               'Fillter2D(img, param, gui=False)'])
        fnc_list.append(partial(Fillter2D))

        proc_code_list.append(['ぼかし (GaussianBlur)',
                               'GaussianBlur(img, param, gui=False)'])
        fnc_list.append(partial(GaussianBlur))

        proc_code_list.append(['二値化 (inRange)',
                               'InRange(img, param, gui=False)'])
        fnc_list.append(partial(InRange))

        proc_code_list.append(['輪郭抽出 (Laplacian)',
                               'Laplacian(img, param, gui=False)'])
        fnc_list.append(partial(Laplacian))

        proc_code_list.append(['ぼかし (MedianBlur)',
                               'MedianBlur(img, param, gui=False)'])
        fnc_list.append(partial(MedianBlur))

        proc_code_list.append(['モルフォロジー (Morphology)',
                               'Morphology(img, param, gui=False)'])
        fnc_list.append(partial(Morphology))

        proc_code_list.append(['回転 (Rotate)',
                               'Rotate(img, param, gui=False)'])
        fnc_list.append(partial(Rotate))

        proc_code_list.append(['輪郭抽出 (Sobel)',
                               'Sobel(img, param, gui=False)'])
        fnc_list.append(partial(Sobel))

        proc_code_list.append(['二値化 (Threshold)',
                               'Threshold(img, param, gui=False)'])
        fnc_list.append(partial(Threshold))

        proc_code_list.append(['切り抜き (Trim)',
                               'Trim(img, param, gui=False)'])
        fnc_list.append(partial(Trim))

        proc_code_list.append(['シャープ (UnSharp)',
                               'UnSharp(img, param, gui=False)'])
        fnc_list.append(partial(UnSharp))

        proc_code_list.append(['明るさ／コントラスト (ConvertScaleAbs)',
                               'ConvertScaleAbs(img, param, gui=False)'])
        fnc_list.append(partial(ConvertScaleAbs))

        proc_code_list.append(['ぼかし (FastNlMeansDenoisingColored)',
                               'FastNlMeansDenoisingColored(img, param, gui=False)'])
        fnc_list.append(partial(FastNlMeansDenoisingColored))

        proc_code_list.append(['ガンマ補正 (Gamma)',
                               'Gamma(img, param, gui=False)'])
        fnc_list.append(partial(Gamma))

        proc_code_list.append(['ホワイトバランス (WhiteBalance)',
                               'WhiteBalance(img, param, gui=False)'])
        fnc_list.append(partial(WhiteBalance))

        proc_code_list.append(['平坦化 (EqualizeHist)',
                               'EqualizeHist(img, param, gui=False)'])
        fnc_list.append(partial(EqualizeHist))

        proc_code_list.append(['色反転 (Bitwise Not)',
                               'BitwiseNot(img, param, gui=False)'])
        fnc_list.append(partial(BitwiseNot))

        proc_code_list.append(['明度反転 (Reverse Brightness)',
                               'ReverseBrightness(img, param, gui=False)'])
        fnc_list.append(partial(ReverseBrightness))

        proc_code_list.append(['濃淡補正 (MovingAve)',
                               'ShadingMovingAve(img, param, gui=False)'])
        fnc_list.append(partial(ShadingMovingAve))

        proc_code_list.append(['濃淡補正 (MovingAveColor)',
                               'ShadingColorMovingAve(img, param, gui=False)'])
        fnc_list.append(partial(ShadingColorMovingAve))

        proc_code_list.append(['濃淡補正 (ShadingApproximate)',
                               'ShadingApproximate(img, param, gui=False)'])
        fnc_list.append(partial(ShadingApproximate))

        proc_code_list.append(['濃淡補正 (ShadingBlur)',
                               'ShadingBlur(img, param, gui=False)'])
        fnc_list.append(partial(ShadingBlur))

        proc_code_list.append(['濃淡補正 (ShadingMediaBlur)',
                               'ShadingMedianBlur(img, param, gui=False)'])
        fnc_list.append(partial(ShadingMedianBlur))

        proc_code_list.append(['濃淡補正 (ShadingColorMedianBlur)',
                               'ShadingColorMedianBlur(img, param, gui=False)'])
        fnc_list.append(partial(ShadingColorMedianBlur))

        proc_code_list.append(['濃淡補正 (ShadingCustomFillter)',
                               'ShadingCustomFillter(img, param, gui=False)'])
        fnc_list.append(partial(ShadingCustomFillter))

        proc_code_list.append(['画像メモリ作成(Create IMG Memory)',
                               'imgLib = CreateImgMemory(img, [img_array, img_names], gui=False)'])
        fnc_list.append(partial(CreateImgMemory))

        proc_code_list.append(['射影変換 (warpPerspective)',
                               'Rotate3D(img, param, gui=False)'])
        fnc_list.append(partial(Rotate3D))

        proc_code_list.append(['画像メモリI/O(MemoryIO)',
                               'MemoryIO(img, param, gui=False)'])
        fnc_list.append(partial(MemoryIO))

        proc_code_list.append(['画像結合 (ImageCombine)',
                               'ImageCombine(img, param, gui=False)'])
        fnc_list.append(partial(ImageCombine))

        proc_code_list.append(['濃淡補正 (ShadingMediaBlurColor)',
                               'ShadingColorMedianBlur(img, param, gui=False)'])
        fnc_list.append(partial(ShadingColorMedianBlur))

        proc_code_list.append(['位置合わせ (PhaseCorrelate)',
                               'PhaseCorrelate(img, param, gui=False)'])
        fnc_list.append(partial(PhaseCorrelate))

        proc_code_list.append(['位置合わせ (PhaseCorrelate_XY)',
                               'PhaseCorrelateXY(img, param, gui=False)'])
        fnc_list.append(partial(PhaseCorrelateXY))

        proc_code_list.append(['マスク処理 (Mask)',
                               'Mask(img, param, gui=False)'])
        fnc_list.append(partial(Mask))

        proc_code_list.append(['最小外接円計測 (CircleDetection)',
                               'CircleDetection(img, param, gui=False)'])
        fnc_list.append(partial(CircleDetection))

        proc_code_list.append(['エッジ位置計測 (EdgeMeasurement)',
                               'EdgeMeasurement(img, param, gui=False)'])
        fnc_list.append(partial(EdgeMeasurement))

        proc_code_list.append(['輪郭抽出 (LaplacianCustom)',
                               'LaplacianCustom(img, param, gui=False)'])
        fnc_list.append(partial(LaplacianCustom))

        proc_code_list.append(['エッジ位置_カスタム (Edge_Custom)',
                               'EdgeCustom(img, param, gui=False)'])
        fnc_list.append(partial(EdgeCustom))

        proc_code_list.append(['エッジ円周 (EdgeArc)',
                               'EdgeArc(img, param, gui=False)'])
        fnc_list.append(partial(EdgeArc))

        self.set_proc_code(proc_code_list, fnc_list)

    def run(self):
        self.appwindow.mainloop()


if __name__ == "__main__":
    app = App()
    app.run()
