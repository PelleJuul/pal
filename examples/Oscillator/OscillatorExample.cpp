#include "pal/pal.h"

using namespace pal;

int main(int argc, char **argv)
{
    RealTimeAudio audio;
    Oscillator osc;
    osc.setType(Oscillator::Type::Triangle);

    audio.callback = [&](int numSamples, int numChannels, float *in, float *out)
    {
        for (int sample = 0; sample < numSamples; sample++)
        {
            // Compute your sample here.
            float y = osc.getNext();

            for (int channel = 0; channel < numChannels; channel++)
            {
                // Write it to the output array here.
                out[sample * numChannels + channel] = y;
            }
        }
    };

    Gui gui(800, 600, "New pal project");

    while (gui.draw())
    {
        ImGui::SetNextWindowSize(ImVec2(350, 0), ImGuiCond_FirstUseEver);
        ImGui::Begin("Audio Setup");
        audio.draw();
        ImGui::End();

        ImGui::Begin("Oscillator");
        osc.draw();
        ImGui::End();

        // Uncomment this to see all the available UI widgets.
        // ImGui::ShowDemoWindow();
    }

    return 0;
}