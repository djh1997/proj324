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

# Initial mock-up of design ![initial mock-up image](initial_design.svg)

# Final mock-up ![final mock-up design image](final_design_plan.svg)

So, once I have removed the backlight from the LCD's I can mount them in a frame. I can then begin to control the contrast/pixel density to make them dim. I will then add a LDR to automate the brightness selection, this will remove the manual adjust however I will leave the buttons to set the levels. Next I will add a camera to the system so that the system can also detect bright points hence make a matching point darker on the lens. I will then use the buttons to make it so that you can swap between the modes. The final additional feature I would like to add is some intelligence on the camera side to ignore certain circumstances such as car tail/headlights

# VHDL/FPGA(de o nano) vs. arm(stm32 vs. RPI)

I am currently undecided on the compute platform.

I'm leaning towards the arm side since the camera will likely be 30-60 fps and I believe that the arm will be quick enough. Also I think it will have better support for interfacing the camera and LCD also the STM boards have analogue io for the LDR and contrast for the LCD

After talking to my supervisor and lab tech they both recommended the raspberry pi as the platform. this recommendation is because of the price point of the zero w and the zero cam being so low and the large product support for the increased range of screens possible the only issue with this will be the fact the pi doesn't have analogue io so the dimming of the LCD will be harder but this should be easily worked around.

| component                  | quantity | price(£)        | component type | chosen |
| -------------------------- | -------- | --------------- | -------------- | ------ |
| pi zero w                  | 1        | 9.60            | compute        | yes    |
| pi 3                       | 1        | 35              | compute        | no     |
| stm32                      | 1        | 18.11           | compute        | no     |
| de0nano                    | 1        | 67.16 to 84.46  | compute        | no     |
| MCT0144C6W128128PML        | 2        | 7.57            | lens           | no     |
| DD-12864YO-3A              | 2        | 16.12           | lens           | no     |
| AF 1.8" TFT ST7735R driver | 2        | 10              | lens           | yes    |
| pi zero camera             | 1        | 15              | camera         | yes    |
| pi camera                  | 1        | 24              | camera         | no     |
| ov7670                     | 1        | 5 to 10         | camera         | no     |
| ov7720                     | 1        | .50 from ps eye | camera         | no     |
| DAC 0800                   | 1        | 1.15.           | DAC for LCD    | yes    |
| ZN439                      | 1        | 2.50            | ADC for LDR    | yes    |
