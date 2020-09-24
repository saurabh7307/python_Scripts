try:
    from pytube import YouTube  # pip3 install pytube3
    from pytube import Playlist
except Exception as exception:
    print("Some module missing {} " + str(exception))

url = input("Enter the url of Youtube Video : ")
try:
    ytd = YouTube(url).streams.filter()
    print(ytd)
except Exception as exception:
    print("Some error occur while downloading the video : " + str(exception))
