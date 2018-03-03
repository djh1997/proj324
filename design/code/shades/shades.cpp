#include <ctime>
#include <unistd.h>
#include <fstream>
#include <iostream>
#include <sstream>
#include <raspicam/raspicam.h>

#include <sys/time.h>
class Timer{
    private:
    struct timeval _start, _end;

public:
    Timer(){}
    void start(){
        gettimeofday(&_start, NULL);
    }
    void end(){
        gettimeofday(&_end, NULL);
    }
    double getSecs(){
    return double(((_end.tv_sec  - _start.tv_sec) * 1000 + (_end.tv_usec - _start.tv_usec)/1000.0) + 0.5)/1000.;
    }

};
size_t framestocapture=100;

using namespace std;

int main ( int argc,char **argv ) {
    Timer timer;
    raspicam::RaspiCam Camera; //Cmaera object
    //Open camera
    cout<<"Opening Camera..."<<endl;
    if ( !Camera.open()) {cerr<<"Error opening camera"<<endl;return -1;}
    //wait a while until camera stabilizes
    cout<<"Sleeping for 3 secs"<<endl;
    sleep(3);
    //capture
    size_t i=0;
    timer.start();
    do{
        Camera.grab();
        //allocate memory
        unsigned char *data=new unsigned char[  Camera.getImageTypeSize ( raspicam::RASPICAM_FORMAT_GRAY )];
        //extract the image in rgb format
        Camera.retrieve ( data,raspicam::RASPICAM_FORMAT_GRAY );//get camera image
        //save
        std::stringstream fn;
        fn<<"image";
        if (i<10) fn<<"0";
        fn<<i<<".ppm";
        std::ofstream outFile ( fn.str(),std::ios::binary );
        outFile<<"P5\n"<<Camera.getWidth() <<" "<<Camera.getHeight() <<" 255\n"; //p5 = greyscale image
        outFile.write ( ( char* ) data, Camera.getImageTypeSize ( raspicam::RASPICAM_FORMAT_GRAY ) );
        //free resrources
        delete data;
    }while(++i<framestocapture);
    timer.end();
    cerr<< timer.getSecs()<< " seconds for "<< framestocapture<< "  frames : FPS " << ( ( float ) ( framestocapture ) / timer.getSecs() ) <<endl;
    return 0;
}
