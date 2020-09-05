#pragma once

namespace pal
{

class Oscillator
{
    public:

    enum Type
    {
        Sine,
        Triangle,
        Square,
        Sawtooth,
        Ramp,
        Noise
    };

    void draw();

    float getNext();

    void setType(Oscillator::Type value) { type = value; };

    private:
    Oscillator::Type type = Oscillator::Type::Sine;
    float sampleRate = 44100;
    float phase = 0;
    float freq = 220;
    float pulseWidth = 0.5;
};

}