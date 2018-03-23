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

So, once I have removed the backlight from the LCD's I can mount them in a frame. I can then begin to control the contrast/pixel density to make them dim. I will then add a LDR to automate the brightness selection, this will remove the manual adjust however I will leave the buttons to set the levels. Next I will add a camera to the system so that the system can also detect bright points hence make a matching point darker on the lens. I will then use the buttons to make it so that you can swap between the modes. The final additional feature I would like to add is some intelligence on the camera side to ignore certain circumstances such as car tail/headlights.

# Report

I got the LCD hooked up and displayed some random spots of different opacity on the screen.

[random point video](log/IMG_1188.TRIM.MOV)

## LCD wiring

| Function | Colour | Pi pins chip side | Pi pin | Colour  | Function |
| -------- | ------ | ----------------- | ------ | ------- | -------- |
| vcc      | orange | 17                | 18     | grey    | rs       |
| sda      | yellow | 19                | 20     | black/p | gnd      |
|          | nc     | 21                | 22     | blue    | reset    |
| scl      | green  | 23                | 24     | white   | cs       |

I tried to install opencv to do the image processing but the install failed. After I spoke to my supervisor he confirmed my suspicion that opencv was too over powered for my project.

So I did some more research around low power blob detection in python and found Skimage which has a function for Determinant of Hessian(doh) blob detection. this was lightweight meaning it should be quick enough the only issue I then had was getting the image from the camera into the right format. Since the doh blob need a numpy array as luck would have it skimage has a built in converter.

With this working a passed it an image from the camera and save the image with a circle around the blob.

![blob circle](log/blobbounding2.png)

I then connected the LCD and got blob detection working with that.

![blob lcd](log/IMG_1190.JPG)

Then I started to convert the shades.py (the file that controls the lcd and camera) and telegrambot.py (the script that enables remote control via a chat client bot) this involved more work than I had initially expected since passing variable around wasn't as easy as I had hoped.

I decided to use telegram to add remote control so that you could adjust the colour of the tint [remote control](https://t.me/smartsheadsfypbot).

## Commands

| Command     | Parameters                           | Description                   |
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
| allowallids | na                                   | toggles if admin id is needed |

After I had all of the system working I bought a 5 button capacitive touch sensor. I then started adding that into the code, So that I would be able to control the glasses with out having to have it connected to the internet.

## Capacitive touch sensor wiring

| Function | Colour | Pi pins chip side | Pi pin | Colour | Function |
| -------- | ------ | ----------------- | ------ | ------ | -------- |
| 3.3v     | nc     | 1                 | 2      | nc     | 5v       |
| button 1 | orange | 3                 | 4      | red    | 5v       |
| button 2 | yellow | 5                 | 6      | black  | gnd      |
| button 3 | green  | 7                 | 8      | blues  | button 4 |
| gnd      | nc     | 9                 | 10     | purple | button 5 |

## Buttons

| Button | Pressed      | Held                |
| ------ | ------------ | ------------------- |
| 1      | scroll tints | reset tint to clear |
| 2      | scroll modes | reset to manual     |
| 3      | debug        | turn off            |
| 4      | stop         | start               |
| 5      | na           | exit                |

## Capacitive touch control

[Mode change](log/capmode.MOV)
[Tint change](log/tint.MOV)
[Debug toggle](log/debug.MOV)

## Future development

My setup is mostly a proof of concept for a full prototype/production model I would use an FPGA with a low quality, high frame rate camera and a bare LCD. With that I would be able to increase the communication speed since the io is the limiting factor on the current setup.

Adding [prescription](https://www.ttp.com/case-studies/electronic_lenses) while taking to course mates about my project one of them mentioned this research which could be a cool addition.

**\<>** by Jo Hawkins using Atom and GitHub
