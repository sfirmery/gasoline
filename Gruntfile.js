module.exports = function(grunt) {

  grunt.initConfig({
    pkg: grunt.file.readJSON('package.json'),
    jshint: {
      files: ['Gruntfile.js'],
      options: {
        // options here to override JSHint defaults
        globals: {
          jQuery: true,
          console: true,
          module: true,
          document: true
        }
      }
    },
    bower: {
      install: {
        options: {
          targetDir: 'gasoline/static/vendors',
          layout: 'byComponent',
          install: true,
          verbose: false,
          cleanTargetDir: true,
          cleanBowerDir: false,
          bowerOptions: {}
        }
      }
    },
    copy: {
      fonts: {
        files: [
          {expand: true, flatten: true, src: ['gasoline/static/vendors/**/fonts/*'], dest: 'gasoline/static/fonts/', filter: 'isFile'},
        ]
      }
    },
  });

  grunt.loadNpmTasks('grunt-contrib-uglify');
  grunt.loadNpmTasks('grunt-contrib-jshint');
  grunt.loadNpmTasks('grunt-contrib-qunit');
  grunt.loadNpmTasks('grunt-contrib-watch');
  grunt.loadNpmTasks('grunt-contrib-concat');
  grunt.loadNpmTasks('grunt-contrib-cssmin');
  grunt.loadNpmTasks('grunt-contrib-copy');
  grunt.loadNpmTasks('grunt-bower-task');

  grunt.registerTask('test', ['jshint', 'qunit']);

//  grunt.registerTask('build', ['jshint', 'qunit', 'concat', 'uglify', 'cssmin']);
  grunt.registerTask('build', ['bower', 'copy:fonts']);
  grunt.registerTask('default', 'build');

};