package mn.edu.must.sqat;

import static org.junit.jupiter.api.Assertions.assertEquals;
import org.junit.jupiter.api.Test;

class BonusMutationKillTest {
    // M2 best=present is wrong after a shorter streak and an interrupted longer streak.
    @Test
    void bonus_restartedStreakMustNotUsePresentForBest() {
        assertEquals(0, DataFlowTargets.bonus(new int[]{1,1,0,1,1,1}, 6));
    }
}
