from typing import List, Tuple
from spacy import Language
from spacy.matcher import Matcher
from spacy.tokens import Doc, Span, Token
from spacy.util import filter_spans
from identify_idioms.builders import IdiomMatcherBuilder

Span.set_extension("idiom_lemma", default=None, type_cls=str)
Token.set_extension("is_idiom", default=False, type_cls=bool)


class MergeIdiomsComponent:
    """
    why define the whole class?
    because It has to maintain a reference to an instance of idiom_matcher.
    """
    def __init__(self, nlp: Language, name: str):
        # these..must be json serializable
        self.nlp = nlp
        self.name = name  # not sure if this will ever be useful
        # reconstruct idiom matcher here - it'll only be executed once
        # what if you build idiom matcher here?
        # yeah, that makes sense - then, you have to include
        # this may take some time, but once done, you don't need to repeat them.
        self.idiom_matcher = self.build_idiom_matcher()

    def __call__(self, doc: Doc) -> Doc:
        # use lowercase version of the doc.
        matches = self.idiom_matcher(doc)
        # longest spans is preferred over short ones.
        # if you keep on having the same errors.. just use this filter helper.
        # TODO: change this so that you use the spacy's ner tag.
        with doc.retokenize() as retokeniser:
            for span in self.spans_to_merge(doc, matches):
                retokeniser.merge(
                    span,
                    attrs={
                        'LEMMA': span._.idiom_lemma.replace(" ", "_"),
                        '_': {
                            # just so we know that they are idioms
                            'is_idiom': True
                        }
                    }
                )
        return doc

    def spans_to_merge(self, doc: Doc, matches: Tuple[int, int, int]) -> List[Span]:
        # get the span candidates
        spans: List[Span] = list()
        for lemma_id, start, end in matches:
            span = doc[start:end]
            # override with the correct lemma
            lemma = self.idiom_matcher.vocab.strings[lemma_id]
            span._.idiom_lemma = lemma
            spans.append(span)
        return filter_spans(spans)

    def build_idiom_matcher(self) -> Matcher:
        idiom_matcher_builder = IdiomMatcherBuilder()
        idiom_matcher_builder.construct(self.nlp.vocab)
        return idiom_matcher_builder.idiom_matcher


# factory method for the component
@Language.factory(
    name="merge_idioms",
    retokenizes=True,  # we are merging, so it does retokenize
)
def create_merge_idiom_component(nlp: Language, name: str) -> MergeIdiomsComponent:
    return MergeIdiomsComponent(nlp, name)
