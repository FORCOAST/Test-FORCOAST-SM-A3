# Test-FORCOAST-SM-A3
Test of SM A3 for containerisation

To build this image: <br />
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
- d : expected decay, default: -4

To run the container: <br />
- "docker run forcoast-sm-a3 $1 $2 $3 $4 $5 $6 $7 $8 $9 $10 $11 $12" all parameters need to be given <br />
- Example with default values: "docker run forcoast-sm-a3 2009 5 9 16 28 5 26 0.75 4.5 0.5 -4"

