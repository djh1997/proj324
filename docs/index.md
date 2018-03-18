# **Final Year Project**

![pi0toChroma logo](pi0toChroma.svg)

# Stage Criteria

This is the criteria I would like to meet, to feel as though I have created a successful project.

| Stage | Name                        | Description                                      |
| ----- | --------------------------- | ------------------------------------------------ |
| 1     | Smart shades                | Make a set of smart sun classes                  |
| 2     | Auto smart shades           | Add LDR to control the opacity                   |
| 3     | Auto smart point shades     | Add camera to make dark point over bright points |
| 4     | Controllable smart shades   | Add options to swap between modes                |
| 5     | Driving/safety improvements | Auto react headlights etc.                       |

## Inspiration

[indie-go-go](https://www.indiegogo.com/projects/ctrl-one-the-smartest-lcd-tint-changing-glasses-smart#/)

[ctrl-eyewear](http://www.ctrl-eyewear.com/)

[pc case](https://www.youtube.com/watch?v=E5d7ynJXiZc)

## Plan

The product's above, along with Paul's lectures last year inspired my idea.

The plan is to use two LCD's with the backlight removed, to create dimmable panels in front of the users eyes. Then eventually I will add a camera to make point control which will block bright spots such as projectors and the sun, and dim them to reduce squinting.

# Final mock-up

![final mock-up design image](final_design_plan.svg)

So, once I have removed the backlight from the LCD's I can mount them in a frame. I can then begin to control the contrast/pixel density to make them dim. I will then add a LDR to automate the brightness selection, this will remove the manual adjust however I will leave the buttons to set the levels. Next I will add a camera to the system so that the system can also detect bright points hence make a matching point darker on the lens. I will then use the buttons to make it so that you can swap between the modes. The final additional feature I would like to add is some intelligence on the camera side to ignore certain circumstances such as car tail/headlights

# Report

I got the LCD hooked up and displayed some random spots of different opacity on the screen

[random point video](log/IMG_1188.TRIM.MOV)

I tried to install opencv to do the image processing built the install failed and after I spoke to my supervisor he confirmed my suspicion that opencv was too over powered for my project.

So I did some more research around low power blob detection in python and found Skimage which has a function for Determinant of Hessian(doh) blob detection which should be quick enough the only issue I then had was getting the image from the camera into the right format since the doh blob need a numpy array as luck would have it skimage has a built in converter.

With this working a passed it an image from the camera and save the image with a circle around the blob.

![blob circle](log/blobbounding2.png)

I then connected the LCD and got blob detection working with that.

![blob lcd](log/IMG_1190.JPG)

Then I started to convert the shades.py (the file that controls the lcd and camera) and telegrambot.py (the script that enables remote control via a chat client bot) this involved more work than I had initially expected since passing variable around wasn't as easy as I had hoped

I decided to use telegram to add remote control so that you could adjust the colour of the tint [remote control](https://t.me/smartsheadsfypbot)

| command     | param                                | Description                   |
| ----------- | ------------------------------------ | ----------------------------- |
| help        | na                                   | show the help menu            |
| pickcolour  | pick from list of tints              | preset tints/colours          |
| pickmode    | pick manual,tint,points or full auto | change current mode           |
| joke        | na                                   | tells a joke                  |
| meme        | na                                   | shows a meme                  |
| tint        | percentage                           | sets the tint of the lenses   |
| image       | na                                   | shows you the current image   |
| up          | na                                   | see if the bot is up          |
| temp        | na                                   | see the CPU temperature       |
| start       | na                                   | starts shades                 |
| stop        | na                                   | stop shades                   |
| exit        | na                                   | exit shades                   |
| reboot      | na                                   | reboot shades                 |
| halt        | na                                   | shutdown shades               |
| uprecords   | na                                   | see up time                   |
| debug       | na                                   | toggles debug                 |
| colourset   | fore/back@0/255,0/255,0/255          | sets the colour of the lenses |
| allowAllIds | na                                   | toggles if user id is needed  |

After I had all of the system working I bought a 5 button capacitive touch sensor and started adding that into the code so that I would be able to control the glasses with out having to have it connected to the internet

| button | pressed      | held                |
| ------ | ------------ | ------------------- |
| 1      | scroll tints | reset tint to clear |
| 2      | scroll modes | reset to manual     |
| 3      | debug        | turn off            |
| 4      | stop         | start               |
| 5      | na           | exit                |

# capacitive touch control

[mode change](log/capmode.MOV)
[tint change](log/tint.MOV)
[debug toggle](log/debug.MOV)
