<http://uk.rs-online.com/web/p/oled-displays/0554314/>

<http://uk.farnell.com/midas/mct0144c6w128128pml/display-tft-lcd-1-44-transmissive/dp/2606862>

# lcd

[pickedlcd](https://www.adafruit.com/product/618)

## pinout

![image](lcd_pinout.png)

lcd pin number | name  | used | colour | pi pin
-------------- | ----- | ---- | ------ | ------
1              | NC    | no   | na     |
2              | gnd   | ?    | purple | 20
3              | ledk  | no   | na     |
4              | leda  | no   | na     |
5              | gnd   | ?    | pink   | 20
6              | reset | yes  | blue   | 22
7              | rs/dc | yes  | grey   | 18
8              | sda   | yes  | yellow | 19
9              | scl   | yes  | green  | 23
10             | vcc   | yes  | orange | 17
11             | vcc   | yes  | na     |
12             | cs    | yes  | white  | 24
13             | gnd   | ?    | black  | 20
14             | NC    | no   | na     |

# lcd maths

![image](lcdfovcalc.png)

$$ { \frac {128} {86.05}} = 1.48 \text{ vertical degrees per pixel}$$

$$ { \frac {160} {98.8}} = 1.62 \text{ vertical degrees per pixel}$$
