// tina/config.tsx
import { defineConfig } from "tinacms";
var config_default = defineConfig({
  branch: "main",
  build: {
    outputFolder: "admin",
    publicFolder: ""
  },
  schema: {
    collections: [
      {
        name: "content",
        label: "Oldal tartalom",
        path: "content",
        format: "json",
        ui: { allowedActions: { create: false, delete: false } },
        fields: [
          {
            type: "object",
            label: "Fejl\xE9c / Hero",
            name: "site",
            fields: [
              { type: "string", label: "Brand (fix)", name: "brand", ui: { readOnly: true } },
              { type: "string", label: "Szerep / alc\xEDm", name: "role" },
              { type: "string", label: "N\xE9v sor 1", name: "hero_line1" },
              { type: "string", label: "N\xE9v sor 2", name: "hero_line2" },
              { type: "string", label: "Hero le\xEDr\xE1s", name: "tagline", ui: { component: "textarea" } },
              {
                type: "object",
                label: "Reel gomb",
                name: "reel",
                fields: [
                  { type: "string", label: "Felirat", name: "label" },
                  { type: "string", label: "Hossz", name: "duration" },
                  { type: "string", label: "Link", name: "href" }
                ]
              },
              { type: "string", label: "E-mail", name: "email" },
              { type: "string", label: "Kontakt sz\xF6veg", name: "contact_line" },
              { type: "string", label: "Helysz\xEDn / el\xE9rhet\u0151s\xE9g", name: "location" },
              {
                type: "object",
                label: "HUD \xE9rt\xE9kek (kamera)",
                name: "hud",
                fields: [
                  { type: "string", label: "FPS", name: "fps" },
                  { type: "string", label: "Shutter", name: "shutter" },
                  { type: "string", label: "Iris", name: "iris" },
                  { type: "string", label: "EI", name: "ei" },
                  { type: "string", label: "ND", name: "nd" },
                  { type: "string", label: "CAM", name: "cam" },
                  { type: "string", label: "FCL", name: "fcl" },
                  { type: "string", label: "Media", name: "media" },
                  { type: "string", label: "TC kezd\u0151\xE9rt\xE9k", name: "tc_start" }
                ]
              }
            ]
          },
          {
            type: "object",
            label: "About",
            name: "about",
            fields: [
              { type: "string", label: "C\xEDmke", name: "label" },
              { type: "string", label: "Helysz\xEDn sor", name: "loc" },
              { type: "string", label: "Nagy mondat", name: "pull", ui: { component: "textarea" } },
              {
                type: "string",
                label: "Bekezd\xE9sek",
                name: "paragraphs",
                list: true,
                ui: { component: "textarea" }
              },
              { type: "string", label: "Kollabor\xE1torok sor", name: "collaborators" }
            ]
          },
          {
            type: "object",
            label: "Kateg\xF3ri\xE1k \xE9s projektek",
            name: "categories",
            list: true,
            ui: { itemProps: (item) => ({ label: item?.title }) },
            fields: [
              { type: "string", label: "C\xEDm", name: "title" },
              { type: "string", label: "Darabsz\xE1m", name: "count" },
              { type: "string", label: "Alc\xEDm", name: "desc" },
              { type: "string", label: "Azonos\xEDt\xF3 (id)", name: "id", ui: { readOnly: true } },
              {
                type: "object",
                label: "Projektek",
                name: "projects",
                list: true,
                ui: { itemProps: (item) => ({ label: item?.title }) },
                fields: [
                  { type: "string", label: "C\xEDm", name: "title" },
                  { type: "string", label: "\xC9v", name: "year" },
                  { type: "string", label: "Meta (m\u0171faj \xB7 szerep)", name: "meta" },
                  { type: "string", label: "Link", name: "href" },
                  { type: "boolean", label: "Placeholder c\xEDmke", name: "placeholder" }
                ]
              }
            ]
          }
        ]
      }
    ]
  }
});
export {
  config_default as default
};
