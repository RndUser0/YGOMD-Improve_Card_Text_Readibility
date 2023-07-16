# YGOMD-Improve_Card_Text_Readibility

## Required tools
* [Python 3](https://www.python.org/downloads/)
* [AssetStudio](https://github.com/Perfare/AssetStudio/releases) - Tool for extracting Unity assets
* [UABEA](https://github.com/nesrak1/UABEA/releases) - Tool for importing a modded file back into a game file

## Location of the Unity files which contain the English CARD_* files used by the game:
* CARD_Desc: .\Yu-Gi-Oh!  Master Duel\LocalData\????????\0000\ab\abda12b1
* CARD_Indx: .\Yu-Gi-Oh!  Master Duel\LocalData\????????\0000\da\da0368f7
* CARD_Name: .\Yu-Gi-Oh!  Master Duel\LocalData\????????\0000\fe\fe4cc0e3

## Preparation
1. Copy the above files into a new folder.
2. Copy all files from this repository into the same folder, except **_find_crypto_key.py** and **README.md** which are not necessary for replacing card text.

## Extracting the files
1. Load all 3 CARD_* files into **Asset Studio** by using drag'n'drop or **File** → **Load Folder**.
2. Click on the **Asset List** tab.
3. Click on **Filter Type** → **TextAsset**.
4. Select the 3 files, then right-click one of them.
5. Select **Export selected assets**.
6. Choose a location and click on **Select folder**.
7. Copy the file **_CARD_decrypt_Desc+Indx+Name_and_split_Desc+Name.py** from this repository into the same folder and run it to decrypt and split 2 of the files to JSON.

## Replacing the card text
1. Run the file **_CARD_Desc_replace.py** to replace the card text.
2. Run the file **_CARD_merge+calc_index.py** to reconvert and reencrypt the files, so the game can read them.

## Importing the modified CARD_* files back into the Unity files.
1. Create a backup of the original Unity file containing the **CARD_Desc** file .
2. Load the original Unity file containing the **CARD_Desc** file into **UABEA** by using drag'n'drop or **File** → **Open**.
3. Click on **Memory**.
4. Click on **Info**.
5. In the **Assets Info** window, select the row with the **TextAsset** type.

![image](https://user-images.githubusercontent.com/4957582/181439832-73631410-bd14-43b5-8c5f-189f36c0615b.png)
  
6. Click on **Plugins** → **Import .txt** → **Ok**.
7. Click on the drop down box to the right saying **bytes files (\*.bytes)** and select **All types (\*.*)**.
8. Select the **CARD_Desc** file.
9. Click on **File** → **Save** → **OK**.
10. Close the **Assets Info** window.
11. In the main **UABEA** window click on **File** → **Save**.
12. Repeat steps 1 to 11 for the **CARD_Indx** file.

## Credits
* [akintos](https://gist.github.com/akintos/04e2494c62184d2d4384078b0511673b) for the decryption script
* [timelic](https://forums.nexusmods.com/index.php?/user/145588218-timelic) for the splitting and merge scripts
* [AmidoriA](https://github.com/AmidoriA) for [the original guide](https://github.com/AmidoriA/Master-Duel-Effect)
* [thenoblethief](https://www.nexusmods.com/yugiohmasterduel/users/26473124) for [the updated Replace Guide.txt](https://cdn.discordapp.com/attachments/1126958884393844798/1129940730077511821/Replace_Guide.txt)

## Links
* [My modding guide on NexusMods](https://www.nexusmods.com/yugiohmasterduel/articles/3)
