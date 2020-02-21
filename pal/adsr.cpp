#include "adsr.h"
#include <cmath>

Adsr::Adsr(float a, float d, float s, float r, float fs)
{
    attack = a;
    decay = d;
    sustain = s;
    rel = r;
    this->fs = fs;
}

float Adsr::next()
{
    if (isTriggered)
    {
        if (timeSinceTrigger < attack)
        {
            value += (1.0 / fs) * (1.0 / attack);
        }
        else if (timeSinceTrigger < attack + decay)
        {
            value -= (1.0 / fs) * (1.0 / attack) * (1.0 - sustain);
        }

        timeSinceTrigger += (1.0 / fs);
    }
    else if (value > 0)
    {
        value -= sustain * (1.0 / fs) * (1.0 / rel);

        timeSinceRelease += (1.0 / fs);
    }
    else if (value < 0)
    {
        value = 0;
    }
    
    return value;
}

void Adsr::release()
{
    if (isTriggered)
    {
        isTriggered = false;
        timeSinceRelease = 0;
    }
}

void Adsr::trigger()
{
    if (!isTriggered)
    {
        isTriggered = true;
        timeSinceTrigger = 0;
    }
}