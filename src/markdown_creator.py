class markdown_creator:
        def write(self,args):
            mdfile = open('bill.md','w')
            for event in args:
                mdfile.write('## Day {}\n'.format(event.date)+
                             'Duration = {:.2f}\n'.format(event.duration)+
                             'Description = {}\n'.format(event.description))
