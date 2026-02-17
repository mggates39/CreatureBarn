import tkinter as tk
from tkinter import ttk


class PairTupleCombobox(ttk.Combobox):
    def _process_list_pair_tuple(self, ip_list_pair_tuple):
        r_list_keys = []
        r_list_shows = []
        for tpl in ip_list_pair_tuple:
            r_list_keys.append(tpl[0])
            r_list_shows.append(tpl[1])
        return r_list_keys, r_list_shows

    def __init__(self, container, p_list_pair_tuple, p_default_key, *args, **kwargs):
        self.i_list_keys, self.i_list_shows = self._process_list_pair_tuple(p_list_pair_tuple)
        super().__init__(container, *args, **kwargs)
        self['values'] = tuple(self.i_list_shows)
        # still need to set the default value from the nominated key
        try:
            t_default_key_index = self.i_list_keys.index(p_default_key)
            self.current(t_default_key_index)
        except:
            pass

    def get_selected_key(self):
        try:
            i_index = self.current()
            return self.i_list_keys[i_index]
        except:
            return None

    def set_selected_key(self, key):
        try:
            t_default_key_index = self.i_list_keys.index(key)
            self.current(t_default_key_index)
        except:
            pass
