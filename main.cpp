#include "pal/pal.h"

int main(int argc, char **argv)
{
    Realtime rt = quickAudio([&](int n, int nc, float *in, float *out)
    {
        for (int i = 0; i < n; i++)
        {
            // Compute your sample here.
            float y = 0;

            for (int c = 0; c < nc; c++)
            {
                // Write it to the output array here.
                out[i * nc + c] = y;
            }
        }
    });

    quickGui([&]()
    {
        ImGui::Begin("New PAL project");
        ImGui::TextWrapped(
            "Congratulations, you have successfully compiled a new pal project."
            "To start developing your application edit the 'main.cpp' file "
            "which already contains the code necessary for this UI and for "
            "real time audio. To see all UI widgets available through ImGui "
            "look at the source code for ImGui::ShowDemoWindow in pal/imgui/"
            "imgui_demo.cpp.\n\nHave a great time using pal! If you find a bug "
            "or have questions please post an issue on github.com/PelleJuul/pal"
        );

        ImGui::End();

        ImGui::ShowDemoWindow();
    });

    rt.stop();

    return 0;
}