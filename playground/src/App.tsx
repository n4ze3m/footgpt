import "./App.css";
import {
  ActionIcon,
  AppShell,
  Button,
  Container,
  Group,
  Header,
  Modal,
  Paper,
  Slider,
  Text,
  TextInput,
} from "@mantine/core";
import { useForm } from "@mantine/form";
import axios from "axios";
import React from "react";
import { useMutation } from "@tanstack/react-query";

function App() {
  const form = useForm({
    initialValues: {
      prompt: "",
      max_new_tokens: 256,
      temperature: 0.7,
      top_p: 0.9,
      freq_penalty: 0,
    },
  });

  const [generatedText, setGeneratedText] = React.useState<string | null>();
  const [open, setOpen] = React.useState(false);

  const onSubmit = async (values: {
    prompt: string;
  }) => {
    const response = await axios.post(
      `${import.meta.env.VITE_API_URL}/generate`,
      values,
    );
    return response.data;
  };

  const {
    isLoading,
    mutateAsync: generateText,
  } = useMutation(onSubmit, {
    onSuccess: (data) => {
      setGeneratedText(data.generated);
    },
  });

  return (
    <AppShell
      padding="md"
      header={
        <Header height={50}>
          <Container
            fluid
            style={{
              display: "flex",
              justifyContent: "space-between",
              alignItems: "center",
              height: "50px",
            }}
          >
            <div
              style={{
                display: "block",
                lineHeight: 1,
                padding: "8px 12px",
              }}
            >
              <Text size="lg" weight="bold">
                FootGPT Playground
              </Text>
            </div>
            <ActionIcon
              component="a"
              href="https://github.com/n4ze3m/footgpt"
              target="_blank"
            >
              <svg
                aria-hidden="true"
                className="h-6 w-6 fill-slate-900"
                viewBox="0 0 24 24"
              >
                <path
                  fillRule="evenodd"
                  fill="#FFFFFF"
                  d="M12 2C6.477 2 2 6.463 2 11.97c0 4.404 2.865 8.14 6.839 9.458.5.092.682-.216.682-.48 0-.236-.008-.864-.013-1.695-2.782.602-3.369-1.337-3.369-1.337-.454-1.151-1.11-1.458-1.11-1.458-.908-.618.069-.606.069-.606 1.003.07 1.531 1.027 1.531 1.027.892 1.524 2.341 1.084 2.91.828.092-.643.35-1.083.636-1.332-2.22-.251-4.555-1.107-4.555-4.927 0-1.088.39-1.979 1.029-2.675-.103-.252-.446-1.266.098-2.638 0 0 .84-.268 2.75 1.022A9.607 9.607 0 0112 6.82c.85.004 1.705.114 2.504.336 1.909-1.29 2.747-1.022 2.747-1.022.546 1.372.202 2.386.1 2.638.64.696 1.028 1.587 1.028 2.675 0 3.83-2.339 4.673-4.566 4.92.359.307.678.915.678 1.846 0 1.332-.012 2.407-.012 2.734 0 .267.18.577.688.48 3.97-1.32 6.833-5.054 6.833-9.458C22 6.463 17.522 2 12 2z"
                  clipRule="evenodd"
                >
                </path>
              </svg>
            </ActionIcon>
          </Container>
        </Header>
      }
      footer={
        <div>
          <Text size="xs" color="dimmed">
            This is a demo of the FootGPT model. Model will generate random
            bullsh*ts please don't take it seriously.
          </Text>
        </div>
      }
    >
      <Container>
        <form onSubmit={form.onSubmit((values) => generateText(values))}>
          <TextInput
            required
            placeholder="Write something here..."
            {...form.getInputProps("prompt")}
            rightSection={
              <ActionIcon
                onClick={() => setOpen(true)}
              >
                <svg
                  xmlns="http://www.w3.org/2000/svg"
                  fill="none"
                  viewBox="0 0 24 24"
                  strokeWidth={1.5}
                  stroke="currentColor"
                  className="w-6 h-6"
                >
                  <path
                    strokeLinecap="round"
                    strokeLinejoin="round"
                    d="M9.594 3.94c.09-.542.56-.94 1.11-.94h2.593c.55 0 1.02.398 1.11.94l.213 1.281c.063.374.313.686.645.87.074.04.147.083.22.127.324.196.72.257 1.075.124l1.217-.456a1.125 1.125 0 011.37.49l1.296 2.247a1.125 1.125 0 01-.26 1.431l-1.003.827c-.293.24-.438.613-.431.992a6.759 6.759 0 010 .255c-.007.378.138.75.43.99l1.005.828c.424.35.534.954.26 1.43l-1.298 2.247a1.125 1.125 0 01-1.369.491l-1.217-.456c-.355-.133-.75-.072-1.076.124a6.57 6.57 0 01-.22.128c-.331.183-.581.495-.644.869l-.213 1.28c-.09.543-.56.941-1.11.941h-2.594c-.55 0-1.02-.398-1.11-.94l-.213-1.281c-.062-.374-.312-.686-.644-.87a6.52 6.52 0 01-.22-.127c-.325-.196-.72-.257-1.076-.124l-1.217.456a1.125 1.125 0 01-1.369-.49l-1.297-2.247a1.125 1.125 0 01.26-1.431l1.004-.827c.292-.24.437-.613.43-.992a6.932 6.932 0 010-.255c.007-.378-.138-.75-.43-.99l-1.004-.828a1.125 1.125 0 01-.26-1.43l1.297-2.247a1.125 1.125 0 011.37-.491l1.216.456c.356.133.751.072 1.076-.124.072-.044.146-.087.22-.128.332-.183.582-.495.644-.869l.214-1.281z"
                  />
                  <path
                    strokeLinecap="round"
                    strokeLinejoin="round"
                    d="M15 12a3 3 0 11-6 0 3 3 0 016 0z"
                  />
                </svg>
              </ActionIcon>
            }
          />

          <Group>
            <Button my="md" color="teal" loading={isLoading} type="submit">
              Generate
            </Button>
          </Group>
        </form>
        {generatedText && (
          <Paper p="md" shadow="sm" withBorder>
            <Text size="lg" align="left">
              {generatedText}
            </Text>
          </Paper>
        )}
      </Container>
      <Modal
        size="lg"
        opened={open}
        onClose={() => setOpen(false)}
        title="Settings"
      >
        <div
          style={{
            marginBottom: "5px",
          }}
        >
          <Group position="apart">
            <Text size="md">
              Maximum length
            </Text>
            {form.getInputProps("max_new_tokens").value}
          </Group>
          <Slider
            min={1}
            max={1000}
            color="teal"
            value={form.getInputProps("max_new_tokens").value}
            onChange={(value) => form.setFieldValue("max_new_tokens", value)}
          />
        </div>
        <div
          style={{
            marginBottom: "5px",
          }}
        >
          <Group position="apart">
            <Text size="md">
              Temperature
            </Text>
            {form.getInputProps("temperature").value}
          </Group>
          <Slider
            min={0.00}
            color="teal"
            max={1.00}
            step={0.01}
            value={form.getInputProps("temperature").value}
            onChange={(value) =>
              form.setFieldValue("temperature", +value.toFixed(3))}
          />
        </div>
        <div
          style={{
            marginBottom: "5px",
          }}
        >
          <Group position="apart">
            <Text size="md">
              Top P
            </Text>
            {form.getInputProps("top_p").value}
          </Group>
          <Slider
            min={0.00}
            color="teal"
            max={1.00}
            step={0.01}
            value={form.getInputProps("top_p").value}
            onChange={(value) => form.setFieldValue("top_p", +value.toFixed(3))}
          />
        </div>
        <div
          style={{
            marginBottom: "5px",
          }}
        >
          <Group position="apart">
            <Text size="md">
              Frequency penalty
            </Text>
            {`${form.getInputProps("freq_penalty").value}`}
          </Group>
          <Slider
            min={0.00}
            color="teal"
            max={1.00}
            step={0.01}
            value={form.getInputProps("freq_penalty").value}
            onChange={(value) =>
              form.setFieldValue("freq_penalty", +value.toFixed(3))}
          />
        </div>
      </Modal>
    </AppShell>
  );
}

export default App;
