import { defineStore } from 'pinia';

export const useUiStore = defineStore('ui', {
  state: () => ({
    isDarkMode: false,
  }),
  actions: {
    initTheme() {
      const storedTheme = localStorage.getItem('theme');
      if (storedTheme) {
        this.isDarkMode = storedTheme === 'dark';
      } else {
        this.isDarkMode = window.matchMedia('(prefers-color-scheme: dark)').matches;
      }
      this.applyTheme();
    },
    toggleDarkMode() {
      this.isDarkMode = !this.isDarkMode;
      this.applyTheme();
    },
    applyTheme() {
        if (this.isDarkMode) {
            document.documentElement.classList.add('dark');
            localStorage.setItem('theme', 'dark');
        } else {
            document.documentElement.classList.remove('dark');
            localStorage.setItem('theme', 'light');
        }
    }
  },
});
