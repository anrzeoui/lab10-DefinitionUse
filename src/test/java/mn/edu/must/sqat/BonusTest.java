package mn.edu.must.sqat;

import static org.junit.jupiter.api.Assertions.*;
import org.junit.jupiter.api.Test;

/** Additional test inputs selected from the def-clear DU-pair table. */
class BonusTest {
    @Test
    void bonus_null_throws() {
        assertThrows(IllegalArgumentException.class, () -> DataFlowTargets.bonus(null, 0));
    }
    @Test
    void bonus_negativeThr_throws() {
        assertThrows(IllegalArgumentException.class, () -> DataFlowTargets.bonus(new int[]{}, -1));
    }
    @Test
    void bonus_emptyZero_returns5() {
        assertEquals(5, DataFlowTargets.bonus(new int[]{}, 0));
    }
    @Test
    void bonus_emptyOne_returns0() {
        assertEquals(0, DataFlowTargets.bonus(new int[]{}, 1));
    }
    @Test
    void bonus_absentZero_returns5() {
        assertEquals(5, DataFlowTargets.bonus(new int[]{0,0}, 0));
    }
    @Test
    void bonus_gapBelow_returns0() {
        assertEquals(0, DataFlowTargets.bonus(new int[]{1,1,0,1}, 5));
    }
    @Test
    void bonus_gapMeets_returns5() {
        assertEquals(5, DataFlowTargets.bonus(new int[]{1,0,1}, 2));
    }
    @Test
    void bonus_longBelow_returns3() {
        assertEquals(3, DataFlowTargets.bonus(new int[]{1,1,1,1,1}, 6));
    }
    @Test
    void bonus_zeroThrLong_returns8() {
        assertEquals(8, DataFlowTargets.bonus(new int[]{1,1,1,1,1}, 0));
    }
    @Test
    void bonus_onePositiveBelow_returns0() {
        assertEquals(0, DataFlowTargets.bonus(new int[]{1}, 2));
    }
}
