# Test-FORCOAST-SM-A3
Test of SM A3 for containerisation

To build this image: <br />
-Make sure run.sh EOL is in Unix <br />
-Open cmd or powershell with Docker running <br />
-cd %directory of the dockerfile% <br />
-Then run the command: "docker build -t forcoast-sm-a3 ."



Available parameters:  <br />
- years : the input year, default: 2009 <br />
- mb : the first month input, default: 5 <br />
- me : the last month input (it will only run if mb is also given and vice versa), default: 9 <br />
- sl : salinity lower treshold, default: 16 <br />
- su : salinity upper treshold, default: 28 <br />
- tl : temperature lower treshold, default: 5 <br />
- tu : temperature upper treshold, default: 26 <br />
- kf : half saturation contstant for food (mg chl/m3), default: 0.75 <br />
- o : oxygen lower treshold, default: 4.5 <br />
- kr : treshold resuspension (g-POM/m2/d), default: 0.5 <br />
- d : expected decay, default: -4 <br />
- tb : Telegram bot token <br />
- tc : Telegram chat ID <br />
- b : Bulletin to be sent <br />
- m: method, specify file or URL as input <br />
- Wbb: Bounding box west, default: 8.18 <br />
- Ebb: Bounding box east, default: 9.5 <br />
- Sbb: Bounding box south, default: 56.45 <br />
- Nbb: Bounding box north, default: 57.05 <br />

To run the container: <br />
- "docker run forcoast-sm-a3 years mb me sl su tl tu kf o kr d tb tc b m Wbb Ebb Sbb Nbb" all parameters need to be given <br />
- Example with default values: "docker run forcoast-sm-a3 2009 5 9 16 28 5 26 0.75 4.5 0.5 -4 5267228188:AAGx60FtWgHkScBb3ISFL1dp6Oq_9z9z0rw -1001773490347 ./output/bulletin.png file 8.18 9.5 56.45 57.05"

