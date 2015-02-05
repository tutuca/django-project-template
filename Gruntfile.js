module.exports = function(grunt) {
  'use strict';
  grunt.initConfig({
    pkg: grunt.file.readJSON('package.json'),

    sass: {
      options: {
        includePaths: [
          './assets/lib/foundation/scss',
          './assets/lib/foundation-icon-fonts',
        ]
      },
      dist: {
        options: {
          outputStyle: 'compressed'
        },
        files: {
          './static/css/app.css': './assets/scss/app.scss'
        }        
      }
    },
    copy: {
      main: {
        files: [
          {
            flatten:true,
            cwd: './assets/lib/katex/fonts',
            src: ['**'],
            dest: './static/css/fonts/',
            expand: true
          },
          {
            flatten:true,
            cwd: './assets/lib/foundation-icon-fonts',
            src: ['*.ttf', '*.eot', '*.svg', '*.woff'],
            dest: './static/css/fonts/',
            expand: true
          },
        ]
      }
    },
    concat: {
      options: {
        separator: ';',
      },
      lib: {
        src: [
          './assets/lib/foundation/js/vendor/modernizr.js',
          './assets/lib/foundation/js/vendor/jquery.js',
          './assets/lib/foundation/js/vendor/fastclick.js',
          './assets/lib/foundation/js/foundation.js',
          './assets/lib/katex/katex.min.js'
        ],
        dest: './static/js/lib.js'

      },
      main: {
        src: [
          './assets/js/app.js'
        ],
        dest: './static/js/app.js'
      },
      css: {
        src: [ 
          './assets/lib/katex/*.css',
          './static/css/app.css',
        ],
        dest: './static/css/app.css'
      }
    },
    uglify: {
      options: {
        mangle: true,
        sourceMap: true,
      },
      main: {
        files: {
          './static/js/app.min.js': './static/js/app.js',
        }
      }
    },
    watch: {
      lib: {
        files: ['./assets/lib/**/*.js'],
        tasks: ['concat:lib']
      },
      config: {
        files: [
          'Gruntfile.js',
          'bower.json',
          'package.json'
        ],
        tasks: ['copy', 'concat', 'sass']
      },
      main: {
        files: [
         //watched files
          './assets/js/app.js'
        ],   
        tasks: ['concat:main'],
        options: {
          livereload: true
        }
      },
      sass: {
        files: './assets/scss/**/*.scss',
        tasks: ['sass']
      },

    }
  });
  // Plugin loading
  grunt.loadNpmTasks('grunt-contrib-concat');
  grunt.loadNpmTasks('grunt-contrib-watch');
  grunt.loadNpmTasks('grunt-contrib-copy');
  grunt.loadNpmTasks('grunt-contrib-uglify');
  grunt.loadNpmTasks('grunt-sass');

  // Task definition
  grunt.registerTask('build', ['copy', 'sass', 'concat', 'uglify']);
  grunt.registerTask('default', ['build', 'watch']);

};