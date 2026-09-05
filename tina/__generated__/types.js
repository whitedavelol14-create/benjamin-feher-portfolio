export function gql(strings, ...args) {
  let str = "";
  strings.forEach((string, i) => {
    str += string + (args[i] || "");
  });
  return str;
}
export const ContentPartsFragmentDoc = gql`
    fragment ContentParts on Content {
  __typename
  site {
    __typename
    brand
    role
    hero_line1
    hero_line2
    tagline
    reel {
      __typename
      label
      duration
      href
    }
    email
    contact_line
    location
    hud {
      __typename
      fps
      shutter
      iris
      ei
      nd
      cam
      fcl
      media
      tc_start
    }
  }
  about {
    __typename
    label
    loc
    pull
    paragraphs
    collaborators
  }
  categories {
    __typename
    title
    count
    desc
    id
    projects {
      __typename
      title
      year
      meta
      href
      placeholder
    }
  }
}
    `;
export const ContentDocument = gql`
    query content($relativePath: String!) {
  content(relativePath: $relativePath) {
    ... on Document {
      _sys {
        filename
        basename
        hasReferences
        breadcrumbs
        path
        relativePath
        extension
      }
      id
    }
    ...ContentParts
  }
}
    ${ContentPartsFragmentDoc}`;
export const ContentConnectionDocument = gql`
    query contentConnection($before: String, $after: String, $first: Float, $last: Float, $sort: String, $filter: ContentFilter) {
  contentConnection(
    before: $before
    after: $after
    first: $first
    last: $last
    sort: $sort
    filter: $filter
  ) {
    pageInfo {
      hasPreviousPage
      hasNextPage
      startCursor
      endCursor
    }
    totalCount
    edges {
      cursor
      node {
        ... on Document {
          _sys {
            filename
            basename
            hasReferences
            breadcrumbs
            path
            relativePath
            extension
          }
          id
        }
        ...ContentParts
      }
    }
  }
}
    ${ContentPartsFragmentDoc}`;
export function getSdk(requester) {
  return {
    content(variables, options) {
      return requester(ContentDocument, variables, options);
    },
    contentConnection(variables, options) {
      return requester(ContentConnectionDocument, variables, options);
    }
  };
}
import { createClient } from "tinacms/dist/client";
const generateRequester = (client) => {
  const requester = async (doc, vars, options) => {
    let url = client.apiUrl;
    if (options?.branch) {
      const index = client.apiUrl.lastIndexOf("/");
      url = client.apiUrl.substring(0, index + 1) + options.branch;
    }
    const data = await client.request({
      query: doc,
      variables: vars,
      url
    }, options);
    return { data: data?.data, errors: data?.errors, query: doc, variables: vars || {} };
  };
  return requester;
};
export const ExperimentalGetTinaClient = () => getSdk(
  generateRequester(
    createClient({
      url: "http://localhost:4001/graphql",
      queries
    })
  )
);
export const queries = (client) => {
  const requester = generateRequester(client);
  return getSdk(requester);
};
