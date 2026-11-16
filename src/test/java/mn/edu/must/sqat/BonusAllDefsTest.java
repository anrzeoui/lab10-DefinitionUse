package mn.edu.must.sqat;

import static org.junit.jupiter.api.Assertions.assertEquals;
import org.junit.jupiter.api.Test;

class BonusAllDefsTest {
    // Covers score def@49 -> c-use@54, streak def@46 -> c-use@41.
    @Test
    void bonus_defsLongBelow_returns3() {
        assertEquals(3, DataFlowTargets.bonus(new int[]{1,1,1,1,1,0,1}, 7));
    }

    // Covers score def@51 -> c-use@54 and score def@54 -> c-use@56.
    @Test
    void bonus_defsLongMeets_returns8() {
        assertEquals(8, DataFlowTargets.bonus(new int[]{1,1,1,1,1}, 5));
    }
}
