# Getting subtitles from Youtube

This project is used to get available subtitles from Youtube, and save them. If the subtitle is available on Youtube, it can be downloaded. Currently, there are three languages supoorted: English, Japanese, and traditional Chinese.


## Prereuisities

- Python3
- beautifulsoup4==4.4.1
- PyQt5==5.13.1
- PyQt5-sip==4.19.19
- pyqtgraph==0.10.0
- qtconsole==4.4.3
- requests==2.9.1


## Execution

1. After cloning this project, please use the following command to execute.
`python3 getSubtitles.py`

2. Copy the URL of the Youtube video to the editbox.

3. Select the language that are needed to get the subtitle.

4. Click the button `Get subtitle`, if the subtitle of the video is available, the message `Subtitle genrated.` is shown below; otherwise the message is `No subtitles found.`

5. After getting the subtitle, click `Save File` button to choose the location to save the subtitle.

6. `Reset` button is used to clear messages.


## Modification of language

If user wants to get the subtitle of another language, please modify `self.lang = ""` at line `75`, `77`, or `79`. Please refer to `http://www.lingoes.net/en/translator/langcode.htm` to select the language code.