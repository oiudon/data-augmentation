import PySimpleGUI as sg
import numpy as np
from PIL import Image
import glob

# テーマの選択
sg.theme("LightBlue6")

# レイアウトの作成
layout = [[sg.T("◆データ拡張したい画像が格納されたフォルダを選択してください。")],
          [sg.B(" 参照 ", k="btn1"), sg.T(k="txt1", font=(None,8))],
          [sg.T("◆データ拡張の条件を選択してください。")],
          [sg.T("【回転】")],
          [sg.R("回転なし", group_id="rotate", key="rad1", default=True, font=(None,10))],
          [sg.R("反時計回りに90°回転", group_id="rotate", key="rad2", font=(None,10))],
          [sg.R("180°回転", group_id="rotate", key="rad3", font=(None,10))],
          [sg.R("時計回りに90°回転", group_id="rotate", key="rad4", font=(None,10))],
          [sg.T("【上下左右反転】")],
          [sg.CB("上下反転", key="chk1", font=(None,10))],
          [sg.CB("左右反転", key="chk2", font=(None,10))],
          [sg.T("◆データ拡張した画像の保存先フォルダを選択してください。")],
          [sg.B(" 保存先 ", k="btn2"), sg.T(k="txt2", font=(None,8))],
          [sg.B(" 実行 ", k="btn3"), sg.T("", k="txt3")]]
win = sg.Window("一括データ拡張アプリ", layout, font=(None,14), size=(570,430))

# 画像参照フォルダ選択部分の作成
imagespath = None
def loadImageFolder():
    global imagespath
    # 画像参照フォルダの読み込み
    loadname1 = sg.popup_get_folder("画像が格納されたフォルダを選択してください。")
    
    # 画像参照フォルダが選択されなかったらreturnする
    if not loadname1:
        return

    # 画像参照フォルダの確定
    imagespath = loadname1
    win["txt1"].update(imagespath)
    win["txt3"].update("")

# 保存先フォルダ選択部分の作成
savepath = None
def loadSaveFolder():
    global savepath
    # 保存先フォルダの読み込み
    loadname2 = sg.popup_get_folder("保存先フォルダを選択してください。")
    
    # 保存先フォルダが選択されなかったらreturnする
    if not loadname2:
        return

    # 保存先フォルダの確定
    savepath = loadname2
    win["txt2"].update(savepath)
    win["txt3"].update("")

# 実行部分の作成
def execute():
    # 画像参照フォルダが選択されているか確認
    if not imagespath:
        sg.PopupTimed("画像が格納されたフォルダを選択してください。")
        return
    # 保存先フォルダが選択されているか確認
    if not savepath:
        sg.PopupTimed("保存先フォルダを選択してください。")
        return
    # データ拡張の条件が選択されているか確認
    if v["rad1"] ==True and v["chk1"] == False and v["chk2"] == False:
        sg.PopupTimed("データ拡張の条件を選択してください。")
        return

    # データ拡張したい画像をリストへ格納
    files = glob.glob(imagespath + "/*.jpg")
    files += glob.glob(imagespath + "/*.jpeg")
    files += glob.glob(imagespath + "/*.png")
    if not files:
        sg.PopupTimed("フォルダに画像ファイルがありませんでした。")
        return

    # データ拡張の実行
    for i, file in enumerate(files):
        img = np.array(Image.open(file).convert('RGB'))

        # 回転処理
        if v["rad1"] == True:
            pass
        elif v["rad2"] == True:
            img = Image.fromarray(np.rot90(img))
        elif v["rad3"] == True:
            img = Image.fromarray(np.rot90(img, 2))
        else:
            img = Image.fromarray(np.rot90(img, 3))
        
        # 上下左右反転処理
        if v["chk1"] == True:
            img = Image.fromarray(np.flipud(img))
        if v["chk2"] == True:
            img = Image.fromarray(np.fliplr(img))
    
        # データ拡張画像の保存
        try:
            img.save(savepath + "/{0:06d}_augmented.jpg".format(i))
            win["txt3"].update("保存完了")
        except FileNotFoundError:
            sg.PopupTimed("保存先フォルダが見つかりません。")
            return

while True:
    e, v = win.read()
    if e == "btn1":
        loadImageFolder()
    if e == "btn2":
        loadSaveFolder()
    if e == "btn3":
        execute()
    if e == None:
        break
win.close()
