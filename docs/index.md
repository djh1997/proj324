# **Final Year Project**

![pi0toChroma logo](pi0toChroma.svg)

by David Joseph Hawkins

A report submitted to the University of Plymouth in partial fulfilment for the degree of BEng(Hons) Electrical and Electronic Engineering.

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

## LCD

### Wiring

| Function | Colour | Pi pins chip side | Pi pin | Colour  | Function |
| -------- | ------ | ----------------- | ------ | ------- | -------- |
| vcc      | orange | 17                | 18     | grey    | rs       |
| sda      | yellow | 19                | 20     | black/p | gnd      |
|          | nc     | 21                | 22     | blue    | reset    |
| scl      | green  | 23                | 24     | white   | cs       |

## FOV

### LCD

![image](lcd/lcdfovcalc.png) 160x128 pixels

98.8 degrees horizontal, 86.05 degrees vertical field of view

$$ { \\frac {128} {86.05}} = 1.48 \\text{ vertical pixels per degree}$$

$$ { \\frac {160} {98.8}} = 1.62 \\text{ horizontal pixels per degree}$$

### Camera

2592x1944 pixels

53.50 degrees horizontal, 41.41 degrees vertical field of view

$$ { \\frac {1944} {41.41}} = 46.95 \\text{ vertical pixels per degree}$$

$$ { \\frac {160} {98.8}} = 48.45 \\text{ vertical pixels per degree}$$

So this will cause issues since the dot placed on the LCD will end up then the wrong place with out scaling

## Frame

I decided to laser cut the frame since this would be more cost/time effective. Also glasses frames tend to be fairly 2-dimensional. In the following image you can the the design iterations.
Starting with a concept where I would heat the acrylic and bend at the red line meaning that you wouldn't be able to fold them.
After that you can see another fixed design but with a simpler shape this was the first iteration that actually got cut. I found that the lens was going to be to close to the eye and the ribbon cable from the lens was going to dig in to the brow of your nose. This was solved in the 3rd iteration by making the distance between the top of the frame and the top of the nose support forcing the user to wear the glasses further down their nose.
After this I designed a hinging mechanism and readded the curves to make the glasses more comfortable. I also added a mounting bracket for the camera. This was the fame I cut and used for most of the prototyping phase of the project.
For the next two design's I was contemplating adding a backing plate to the pi mount and also added a mount for the capacitive touch sensor. This design was never cut since the pi 0 needs clearance for the solder of the pin headers and the backing might have added to much weight. Furthering the design of the hinge buy squaring of one end to make it more ridged and adding a hole to hold it together

![image](frame/devcycle.png)

## Blob detection

I tried to install opencv to do the image processing but the install failed. After I spoke to my supervisor he confirmed my suspicion that opencv was too over powered for my project.

So I did some more research around low power blob detection in python and found Skimage which has a function for Determinant of Hessian(doh) blob detection. this was lightweight meaning it should be quick enough the only issue I then had was getting the image from the camera into the right format. Since the doh blob need a numpy array as luck would have it skimage has a built in converter.

With this working a passed it an image from the camera and save the image with a circle around the blob.

![blob circle](log/blobbounding2.png)

I then connected the LCD and got blob detection working with that.

![blob lcd](log/IMG_1190.JPG)

## Telegram

Then I started to convert the shades.py (the file that controls the lcd and camera) and telegrambot.py (the script that enables remote control via a chat client bot) this involved more work than I had initially expected since passing variable around wasn't as easy as I had hoped.

I decided to use telegram to add remote control so that you could adjust the colour of the tint [remote control](https://t.me/smartsheadsfypbot).

### Commands

| Command     | Parameters                           | Description                   |
| ----------- | ------------------------------------ | ----------------------------- |
| help        | na                                   | show the help menu            |
| pickcolour  | pick from list of tints              | preset tints/colours          |
| pickmode    | pick manual,tint,points or full auto | change current mode           |
| tint        | percentage                           | sets the tint of the lenses   |
| image       | na                                   | shows you the current image   |
| up          | na                                   | see if the bot is up          |
| temp        | na                                   | see the CPU temperature       |
| start       | na                                   | starts shades                 |
| stop        | na                                   | stop shades                   |
| exit        | admin only                           | exit shades                   |
| reboot      | admin only                           | reboot shades                 |
| halt        | admin only                           | shutdown shades               |
| uprecords   | na                                   | see up time                   |
| debug       | na                                   | toggles debug                 |
| colourset   | fore/back@0/255,0/255,0/255          | sets the colour of the lenses |
| allowallids | admin only                           | toggles if admin id is needed |

After I had all of the system working I bought a 5 button capacitive touch sensor. I then started adding that into the code, So that I would be able to control the glasses with out having to have it connected to the internet.

## Capacitive touch sensor

### Wiring

| Function | Colour | Pi pins chip side | Pi pin | Colour | Function |
| -------- | ------ | ----------------- | ------ | ------ | -------- |
| 3.3v     | nc     | 1                 | 2      | nc     | 5v       |
| button 1 | orange | 3                 | 4      | red    | 5v       |
| button 2 | yellow | 5                 | 6      | black  | gnd      |
| button 3 | green  | 7                 | 8      | blues  | button 4 |
| gnd      | nc     | 9                 | 10     | purple | button 5 |

### Buttons

| Button | Colour | Pressed      | Held                |
| ------ | ------ | ------------ | ------------------- |
| 1      | orange | scroll tints | reset tint to clear |
| 2      | yellow | scroll modes | reset to manual     |
| 3      | green  | debug        | turn off            |
| 4      | blue   | stop         | start               |
| 5      | purple | na           | exit                |

### Capacitive touch control

[Mode change](log/capmode.MOV)
[Tint change](log/tint.MOV)
[Debug toggle](log/debug.MOV)

# Criteria met

I believe my project has meet at least level technology readiness level 4, Even pushing some level 5 criteria as defined by the European Commission.

| level  | definition                                                                                                                        |
| ------ | --------------------------------------------------------------------------------------------------------------------------------- |
| TRL 1. | basic principles observed                                                                                                         |
| TRL 2. | technology concept formulated                                                                                                     |
| TRL 3. | experimental proof of concept                                                                                                     |
| TRL 4. | technology validated in lab                                                                                                       |
| TRL 5. | technology validated in relevant environment (industrially relevant environment in the case of key enabling technologies)         |
| TRL 6. | technology demonstrated in relevant environment (industrially relevant environment in the case of key enabling technologies)      |
| TRL 7. | system prototype demonstration in operational environment                                                                         |
| TRL 8. | system complete and qualified                                                                                                     |
| TRL 9. | actual system proven in operational environment (competitive manufacturing in the case of key enabling technologies; or in space) |

The European Association of Research and Technology Organisations (EARTO)
have a slightly more relevant scale of TRL.

![trl](TRLPROPODESED.png)

I still believe I'm level 4 with aspects of level 5 with this scale.

# Future development

My setup is mostly a proof of concept for a full prototype/production model I would use an FPGA with a low quality, high frame rate camera and a bare LCD. With that I would be able to increase the communication speed since the io is the limiting factor on the current setup.

Adding [prescription](https://www.ttp.com/case-studies/electronic_lenses) while taking to course mates about my project one of them mentioned this research which could be a cool addition.

**\<>** by Jo Hawkins using **Atom** and **GitHub**
