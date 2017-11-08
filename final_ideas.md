# stage criteria

These are the criteria I would like to meet to feel as thought I have ached a successful project.

stage | name                        | description
----- | --------------------------- | ----------------------------------------------
1     | smart shades                | make a set of smart sun classes
2     | auto smart shades           | add LDR to control the opacity
3     | auto smart point shades     | add camera to make dark point over dark points
4     | controllable smart shades   | add options to swap between modes
5     | driving/safety improvements | auto react headlights ect.

## Inspiration

[indiegogo](https://www.indiegogo.com/projects/ctrl-one-the-smartest-lcd-tint-changing-glasses-smart#/)

[ctrl-eyewear](http://www.ctrl-eyewear.com/)

[pc case](https://www.youtube.com/watch?v=E5d7ynJXiZc)

## plan

this product along with Paul's lectures last year inspired the idea.

The plan is to use two LCD's with the backlight removed to create dimmable panels in front of the users eyes. Then eventually add a camera to make point control to block bright spots like projectors and the sun and dim them to reduce squinting.

# initial mock-up of design ![inital mock-up image](initial_design.svg)

# hopeful final mock-up ![final mock-up design image](final_design_plan.svg)

So once I have removed the backlight from the LCD's I can mount them in a frame I can then begin to control the contrast/pixel density to make them dim. I will then add a LDR to automate the brightness selection this will remove the manual adjust but I will Leave the buttons to set the levels. next I will add a camera to the system so that it can also detect bright points and make a matching point darker on the lens. I will then use the buttons to make it so you can swap between the modes. The final feature addition I would like to add is some intelligence on the camera side to ignore certain circumstances like car tail/headlights

# VHDL/FPGA(de o nano) vs. arm(stm32 vs. rpi)

I am currently undecided on the compute platform.

I'm leaning towards the arm side since the camera will likely be 30-120 fps and I believe that the arm will be quick enough. Also I think it will have better support for interfacing the camera and LCD also the STM boards have analogue i-o for the LDR and contrast for the LCD

After talking to my supervisor and lab tech they both recommended the raspberry pi as the platform. this recommendation is because of the price point of the zero w and the zero cam being so low and the large product support for the increased range of screens possible

component                  | quantity | price(£)        | component type | chosen
-------------------------- | -------- | --------------- | -------------- | ------
pi zero                    | 1        | 9.60            | compute        | yes
pi 3                       | 1        | 35              | compute        | no
stm32                      | 1        | 18.11           | compute        | no
de0nano                    | 1        | 67.16 to 84.46  | compute        | no
MCT0144C6W128128PML        | 2        | 7.57            | lens           | no
DD-12864YO-3A              | 2        | 16.12           | lens           | no
AF 1.8" TFT ST7735R driver | 2        | 10              | lens           | yes
pi zero camera             | 1        | 15              | camera         | yes
pi camera                  | 1        | 24              | camera         | no
ov7670                     | 1        | 5 to 10         | camera         | no
ov7720                     | 1        | .50 from ps eye | camera         | no
