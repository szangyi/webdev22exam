module.exports = {
  mode:"jit",
  purge:["../views/*.html"],
  content: [],
  theme: {  
    extend: {
      colors:{
        "blue": "#1DA1F2",
        "darkblue": "#2795D9",
        "lightblue": "#8ECDF8",
        "lighterblue": "#EFF9FF",
        "dark": "#657786",
        "light": "#AAB8C2",
        "lighter": "#E1E8ED",
        "lightest": "#F5F8FA",
        "error": "rgba(228, 0, 0)",
        "lighterror": "rgba(228, 0, 0, 0.31)",
        "success":"rgba(43, 191, 43)",
        "lightsuccess":"rgba(43, 191, 43, 0.31)",
        "modalbackground": "rgba(43, 43, 43, .54)"
      }
    },
  },
  plugins: [],
}
