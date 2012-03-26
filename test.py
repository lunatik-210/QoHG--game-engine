import hotshot, hotshot.stats

stats = hotshot.stats.load("asd.prof")
stats.strip_dirs()
stats.sort_stats('time', 'calls')
stats.print_stats(20)

# to mesure any code
#        import hotshot
#        prof = hotshot.Profile("asd.prof")
#        prof.start()

# your code

#        prof.stop()
#        prof.close()
