
--------------VIRTUAL TRIAL ROOM ------------------

Requirements:

-> Python 3.8
-> python modules
	- opencv-python
	- cvzone
	- socket
	- matplotlib
	- mediapipe
	- os
-> unity hub
-> Csharp

----------------------------------------------------

2D Virtual trial room
path: virtual_trial_room\code\shirt.py

requirements:
-> Python 3.8
-> python modules
	- opencv-python
	- cvzone
	- matplotlib
	- mediapipe
	- os
-----------------------
working of code:

-------IMAGES 
->  PNG images are required
->  clothes pictures is placed in folders 'shirts_img' and 'pants_img'
->  Each image is taken in form of a list as seen on line 31 and 41 under variables 'l_shirt' and 'l_pant'
->  cropping function 'img_crp' is used to remove excessive parts of image that is not a part of the clothes

------BODY_TRACKING
->  'cvzone.PoseModule.PoseDetector()' creates a body map of the human present
->  refer to the image 'body_landmarks' under the path "virtual_trial_room\body_landmarks.jpg" for the points 
	of refrence used for identifying the body part
	pt11 = llst[11]                 #co-ordinates for left shoulder
    pt12 = llst[12]                 #co-ordinates for right shoulder 
    pt24 = llst[24]                 #co-ordinates for left side hip 
    pt23 = llst[23]                 #co-ordinates for right side hip
    pt27 = llst[27]                 #co-ordinates for ankle

------CALCULATION OF BODY DIMENSION AND CLOTH PLACEMENT
->  s_width = int((pt11[0] - pt12[0])*1.9)                #shirt width
	s_height = int((pt24[1] - pt12[1])*1.4)               #shirt height
	p_width = int((pt23[0] - pt24[0])*2)                #pant width
	p_height = int((pt27[1] - pt23[1])*1.5)             #pants height
	
	on line 128 to line 131 is used to find the dynamic height and width of the user based on his position 
	in front of his camera
->  offset ratio is required such that the clothes are properly placed on the user.
	NOTE:
		images of the same dimension is preffered, offset ratio for different size of images will vary
->  once offset is done the peice of cloth is resized to match the user's dimensions as seen on line 138.
	the image is placed on the frame using 'cvzone.overlayPNG' function provided.
	
->  line 149 to line 162 is for the pant section	

-------CHANGE OF SHIRT AND PANT
->  line 83 to 124 is dedicated to change of shirt and pant
	animation of a circle forming is used as buffer using cv2.ellipse function, speed of the animation can 
	be changed by changing value of variable 'speed_e' on line 52
	
	to change shirt to next, place both hands on the top left region
	to change shirt to prev, place both hands on the top right region
	to change pant to next, place both hands on the bottom left region
	to change pant to prev, place both hands on the bottom right region
	
--------------------------------------------------------------------------------------------------

3D virtual trial room
path: virtual_trial_room\code\unity_try.py

requirements:
-> python 3.8
-> python modules:
	- opencv-python
	- cvzone
	- socket
-> unity hub
-> Csharp

-----------------------
working of code:

file: unity_try.py

-> UDP connection is used under 'sockets' module of python with address of ("127.0.0.1", 4990)

->  'cvzone.PoseModule.PoseDetector()' creates a body map of the human present
->  refer to the image 'body_landmarks' under the path "virtual_trial_room\body_landmarks.jpg" for the points 
	of refrence used for identifying the body part
->  landmark positions are stored in 'llst' and are converted into a string such that it can be sent to unity as seen 
	in line 26 to 29.
	
file UDPReceive.cs:

->  Required for connection between .py and unity
-> change port number on line 13

file Body_tracking.cs:

->  public UDPReceive udpReceive;  establishes the connection
->  public GameObject[] bodypoints;  body landmark points values will be stored here
->  line 18 to 22 is used to convert the string data into readable list values that can be used
->  line 24 to 28 is required by unity to place the points on the screen in the 3D view
->  transform.position is the property under 3D sphere to place the point is a specific location, the values collected 
	from the data will be directly placed here

-------UNITY 3D core
->  create a module called 'manager' if not created
->  click and drag UDPReceive.cs into the manager and change port number to whatever you wish it to be

->  Create new module called 'body' and create a sub folder to store all points that we will create
->  Create a new 3D object of sphere shape of 0.2 size in terms of scale. create 33 of these points as there are
	33 landmarks of human body
->  drag the Body_tracking.cs script to manager so that it is accessible
->  drag all points under 'body' to manager under body_tracking so that points are accessible from manager

->  Run the unity screen after the unity_try.py to see the results
