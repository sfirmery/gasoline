module.exports = (grunt) ->

  grunt.initConfig
    pkg: grunt.file.readJSON("package.json")

    bower:
      install:
        options:
          targetDir: "gasoline/static/vendors"
          layout: "byComponent"
          install: true
          verbose: false
          cleanTargetDir: true
          cleanBowerDir: false
          bowerOptions: {}

    copy:
      fonts:
        files: [
          expand: true
          flatten: true
          cwd: "gasoline/static/vendors/"
          src: ["**/fonts/*"]
          dest: "gasoline/static/fonts/"
          filter: "isFile"
        ]

      jst:
        files: [
          expand: true
          cwd: "src/frontend/backbone/"
          src: ["**/templates/*.jst"]
          dest: "gasoline/static/js/backbone/"
          filter: "isFile"
        ]

    coffee:
      compile:
        options:
          bare: false
        files: [
          expand: true
          cwd: "src/frontend/"
          src: ['*.coffee', '**/*.coffee']
          dest: "gasoline/static/js/"
          ext: ".js"
          extDot: "first"
        ]

    watch:
      grunt:
        files: ['Gruntfile.coffee']
        options:
          reload: true
      coffee:
        files: ['src/frontend/*.coffee', 'src/frontend/**/*.coffee']
        tasks: ['newer:coffee:compile']
        options:
          debounceDelay: 50
      jst:
        files: ['src/frontend/*.jst', 'src/frontend/**/*.jst']
        tasks: ['newer:copy:jst']
        options:
          debounceDelay: 50

  grunt.loadNpmTasks "grunt-contrib-uglify"
  grunt.loadNpmTasks "grunt-contrib-watch"
  grunt.loadNpmTasks "grunt-contrib-concat"
  grunt.loadNpmTasks "grunt-contrib-cssmin"
  grunt.loadNpmTasks "grunt-contrib-copy"
  grunt.loadNpmTasks "grunt-contrib-coffee"
  grunt.loadNpmTasks "grunt-bower-task"
  grunt.loadNpmTasks "grunt-newer"

  grunt.registerTask "jst", "copy:jst"
  
  grunt.registerTask "build", [
    "bower"
    "copy:fonts"
    "coffee"
    "jst"
  ]
  grunt.registerTask "default", "build"
  return