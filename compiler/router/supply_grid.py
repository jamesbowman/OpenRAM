import debug
from vector3d import vector3d
from grid import grid
from grid_path import grid_path
from direction import direction


class supply_grid(grid):
    """
    A two layer routing map. Each cell can be blocked in the vertical
    or horizontal layer.
    """

    def __init__(self, ll, ur, track_width):
        """ Create a routing map of width x height cells and 2 in the z-axis. """
        grid.__init__(self, ll, ur, track_width)
        
        # Current rail
        self.rail = []

    def reinit(self):
        """ Reinitialize everything for a new route. """

        # Reset all the cells in the map
        for p in self.map.values():
            p.reset()
        

    def find_start_wave(self, wave, width, direct):
        """ 
        Finds the first loc  starting at loc and up that is open.
        Returns None if it reaches max size first.
        """
        # Don't expand outside the bounding box
        if wave[0].x > self.ur.x:
            return None
        if wave[-1].y > self.ur.y:
            return None

        while wave and self.is_wave_blocked(wave):
            wf=grid_path(wave)
            wave=wf.neighbor(direct)
            # Bail out if we couldn't increment futher
            if wave[0].x > self.ur.x or wave[-1].y > self.ur.y:
                return None
            # Return a start if it isn't blocked
            if not self.is_wave_blocked(wave):
                return wave
                
        return wave
    
        
    def is_wave_blocked(self, wave):
        """
        Checks if any of the locations are blocked
        """
        for v in wave:
            if self.is_blocked(v):
                return True
        else:
            return False

    
    def probe(self, wave, direct):
        """
        Expand the wave until there is a blockage and return
        the wave path.
        """
        wave_path = grid_path()
        while wave and not self.is_wave_blocked(wave):
            if wave[0].x > self.ur.x or wave[-1].y > self.ur.y:
                break
            wave_path.append(wave)
            wave = wave_path.neighbor(direct)

        return wave_path

    
