# for more information, see https://gist.github.com/alvations/e1df0ba227e542955a8a

# download and unzip pos tagger library
wget http://nlp.stanford.edu/software/stanford-postagger-full-2015-12-09.zip
unzip stanford-postagger-full-2015-12-09.zip

# download and unzip parser library
wget http://nlp.stanford.edu/software/stanford-parser-full-2015-12-09.zip
unzip stanford-parser-full-2015-12-09.zip

# set env vars
export STANFORDTOOLSDIR=`pwd`
export CLASSPATH=$CLASSPATH:$STANFORDTOOLSDIR/stanford-postagger-full-2015-12-09/stanford-postagger.jar:$STANFORDTOOLSDIR/stanford-parser-full-2015-12-09/stanford-parser.jar:$STANFORDTOOLSDIR/stanford-parser-full-2015-12-09/stanford-parser-3.6.0-models.jar
export STANFORD_MODELS=$STANFORDTOOLSDIR/stanford-postagger-full-2015-12-09/models
