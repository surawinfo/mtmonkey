#!/usr/bin/env perl

use warnings;
use strict;
use CS::Segment;

BEGIN { $| = 1 }

my $PARAMS = {
    use_paragraphs => 1,
    use_lines => 0,
    detect_lists => 100,
    limit_words => 250,
};

my $line = 0;
while (my $text = <STDIN>) {
    if ($text eq "<__DOCUMENT_END__>\n") {
        print "\n<__DOCUMENT_END__>\n";
    }
    else {
    	if ($line > 0) {
    		print "\n<__EXTERNAL_SPLIT__>\n";
    	}
        my @segs = CS::Segment::get_segments($text, $PARAMS);
        print join "\n", @segs;
    }
    $line++;
}
