package mn.edu.must.sqat;

import static org.junit.jupiter.api.Assertions.assertEquals;
import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;

class GcdTest {
    @Test
    @DisplayName("gcd DU zero loop: x 13-20, y 13-15F")
    void gcd_zeroLoop_x13_to20() {
        assertEquals(7, DataFlowTargets.gcd(7, 0));
    }

    @Test
    @DisplayName("gcd DU two loops: x 17-16/20, y 18-15/16/17, tmp 16-18")
    void gcd_twoLoops_x17_to16() {
        assertEquals(4, DataFlowTargets.gcd(12, 8));
    }
}
