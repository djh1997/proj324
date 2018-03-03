
#include <raspicam/raspicam.h>
int main(int argc, char **argv)
{
raspicam::RaspiCam Camera;
Camera.grab();
Camera.retrieve ( image);
Camera.release();
}
