# stage criteria

These are the criteria I would like to meet to feel as thought I have ached a successful project.

stage | name                        | description
----- | --------------------------- | ---------------------------------------------------------
1     | smart shades                | make a set of smart sun classes
2     | variable smart shades       | make a set of smart sun classes with controllable opacity
3     | auto smart shades           | add LDR to control the opacity
4     | auto smart point shades     | add camera to make dark point over dark points
5     | controllable smart shades   | add options to swap between modes
6     | driving/safety improvements | auto react headlights ect.

## Inspiration

[indiegogo](https://www.indiegogo.com/projects/ctrl-one-the-smartest-lcd-tint-changing-glasses-smart#/)

[ctrl-eyewear](http://www.ctrl-eyewear.com/)

[pc case](https://www.youtube.com/watch?v=E5d7ynJXiZc)

## plan

These product's along with Paul's lectures last year inspired the idea.

The plan is to use two LCD's with the backlight removed to create dimmable panels in front of the users eyes. Then eventually add a camera to make point control to block bright spots like projectors and the sun and dim them to reduce squinting.

# initial mockup of design ![inital mockup image](initial_design.svg)

# hopefull final mockup ![final mockup design image](final_design_plan.svg)

So once I have removed the backlight from the LCD's I can mount them in a frame I can then begin to control the contrast/pixel density to make them dim. I will then add a LDR to automate the brightness selection this will remove the manual adjust but I will Leave the buttons to set the levels. next I will add a camera to the system so that it can also detect bright points and make a matching point darker on the lens. I will then use the buttons to make it so you can swap between the modes. The final feature addition I would like to add is some intelligence on the camera side to ignore certain circumstances like car tail/headlights

# VHDL vs. arm

I am currently undecided on the compute platform.

I'm leaning towards the arm side since the camera will likely be 30-120 fps and I believe that the arm will be quick enough. Also I think it will have better support for interfacing the camera and LCD also the STM boards have analogue io for the LDR and contrast for the LCD
