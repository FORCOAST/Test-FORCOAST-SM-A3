# ForCoast-SM-A3

### Description

This service identifies areas with the highest growth potential and lowest mortality for flat 
oysters, Ostrea edulis, and thereby increase harvest and restoration potential. The model can be fine-tuned by tweaking service parameters based on local knowledge or literature data. The service will produce a map containing a site suitability index. 

### How to run

* Containerize contents in docker
* Run the command Docker run forcoast/forcoast-sm-a1 &lt;yb> &lt;ye> &lt;mb> &lt;me> &lt;sl> &lt;su> &lt;tl> &lt;tu> &lt;kf> &lt;o> &lt;kr> &lt;d> &lt;tb> &lt;tc> &lt;b> &lt;m> &lt;Wbb> &lt;Ebb> &lt;Sbb> &lt;Nbb> &lt;Telegram token> &lt;Telegram chat-id>
Available parameters:  <br />
  * yb : the first year, default: 2009
  * ye : the last year, default: 2011
  * mb : the first month input, default: 5 
  * me : the last month input (it will only run if mb is also given and vice versa), default: 9 
  * sl : salinity lower treshold, default: 16
  * su : salinity upper treshold, default: 28
  * tl : temperature lower treshold, default: 5 
  * tu : temperature upper treshold, default: 26 
  * kf : half saturation contstant for food (mg chl/m3), default: 0.75 
  * o : oxygen lower treshold, default: 4.5 
  * kr : treshold resuspension (g-POM/m2/d), default: 0.5 
  * d : expected decay, default: -4 
  * tb : Telegram bot token 
  * tc : Telegram chat ID 
  * b : Bulletin to be sent
  * m: method, specify file or URL as input
  * Wbb: Bounding box west, default: 8.18
  * Ebb: Bounding box east, default: 9.5 
  * Sbb: Bounding box south, default: 56.45 
  * Nbb: Bounding box north, default: 57.05 
  * Telegram bot is used for sending the bulletins through messaging services
* Example of use: Docker run docker run forcoast-sm-a3 2009 2011 5 9 16 28 5 26 0.75 4.5 0.5 -4 5267228188:AAGx60FtWgHkScBb3ISFL1dp6Oq_9z9z0rw -1001773490347 ./output/bulletin.png file 8.18 9.5 56.45 57.05

### Licence

Licensed under the Apache License, Version 2.0

