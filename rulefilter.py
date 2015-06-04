from csv_unicode import UnicodeDictReader, UnicodeDictWriter
import os
import codecs

from commons import dialect, src_name, out_name


rulebook_id_header = 'rulebook_id'

class RuleFileFilter:
    def __init__(self, filename, srcdir, outdir, book_selection):
        if not os.path.exists(outdir):
            os.makedirs(outdir)
        self.filename = filename
        self.inpath = os.path.join(srcdir, filename)
        self.outpath = os.path.join(outdir, filename)
        self.book_selection = book_selection

    def init_io(self, infile, outfile):
        reader = UnicodeDictReader(infile, dialect=dialect)
        writer = UnicodeDictWriter(outfile, reader.header, dialect=dialect)
        writer.writeheader()
        return reader, writer

    def filter_rows(self, reader, writer):
        for row in reader:
            book_id = row[rulebook_id_header]
            if book_id in self.book_selection:
                writer.writerow(row)

    def filter(self):
        with codecs.open(self.inpath, 'r') as infile, codecs.open(self.outpath, 'w+') as outfile:
            reader, writer = self.init_io(infile, outfile)
            self.filter_rows(reader, writer)


class RuleFilter:
    def __init__(self, basedir, book_selection):
        self.basedir = basedir
        self.book_selection = book_selection
        self.srcdir = os.path.join(basedir, src_name)
        self.outdir = os.path.join(basedir, out_name)

    def has_rulebook_header(self, filename):
        filepath = os.path.join(self.srcdir, filename)
        with codecs.open(filepath, 'r') as file:
            reader = UnicodeDictReader(file, dialect=dialect)
            return rulebook_id_header in reader.header

    def files_with_rulebook(self):
        for root, dirs, files in os.walk(self.srcdir):
            files_with_rulebook = filter(self.has_rulebook_header, files)
            return list(files_with_rulebook)

    def filter_rule_files(self):
        for filename in self.files_with_rulebook():
            filefilter = RuleFileFilter(filename, self.srcdir, self.outdir, self.book_selection)
            filefilter.filter()


